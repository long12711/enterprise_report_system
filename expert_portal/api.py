import os
import json
import uuid
from datetime import datetime, timedelta

import pandas as pd
from flask import Blueprint, jsonify, session, redirect, request, current_app
from werkzeug.utils import secure_filename

from .services.matcher import get_expert_matches, _compute_score_from_excel

api_bp = Blueprint("expert_api", __name__)


# ============== 会话校验 ==============
@api_bp.before_request
def _ensure_expert_role_api():
    """仅允许专家角色访问专家门户 API"""
    if session.get("role") != "expert":
        return redirect("/")


# ============== 通用工具 ==============
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
STORAGE_DIR = os.path.join(ROOT_DIR, "storage")
SUBMISSION_DIR = os.path.join(STORAGE_DIR, "submissions")
REPORT_DIR = os.path.join(STORAGE_DIR, "reports")
LEDGER_DIR = os.path.join(STORAGE_DIR, "expert_ledgers")
FEEDBACK_DIR = os.path.join(STORAGE_DIR, "expert_feedbacks")
REVIEW_DIR = os.path.join(STORAGE_DIR, "enterprise_reviews")
PROFILE_DIR = os.path.join(STORAGE_DIR, "expert_profiles")

for _d in [SUBMISSION_DIR, REPORT_DIR, LEDGER_DIR, FEEDBACK_DIR, REVIEW_DIR, PROFILE_DIR]:
    os.makedirs(_d, exist_ok=True)


RATING_LEVELS = {"local", "provincial", "national"}


def _now_ts():
    return datetime.utcnow().isoformat(timespec="seconds")


def _ts_text(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ts


def _load_json(path: str, default):
    try:
        if not os.path.exists(path):
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def _save_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============== 专家档案与评级 ==============
def _profile_path(username: str) -> str:
    return os.path.join(PROFILE_DIR, f"{username}.json")


def _default_profile() -> dict:
    lvl = session.get("user_level") or ""
    if lvl == "senior":
        rating = "national"
    elif lvl == "intermediate":
        rating = "provincial"
    else:
        rating = "local"

    return {
        "display_name": session.get("display_name") or "",
        "level": lvl,
        "email": "",
        "phone": "",
        "org": "",
        "title": "",
        "expertise": "",
        "bio": "",
        "rating_level": rating,
        "province": "",
        "city": "",
        "district": "",
        "categories": [],
    }


def _get_expert_profile() -> dict:
    username = session.get("username") or "anonymous"
    prof = _load_json(_profile_path(username), None)
    if not prof:
        prof = _default_profile()

    cats = prof.get("categories")
    if isinstance(cats, str):
        prof["categories"] = [c.strip() for c in cats.replace("，", ",").split(",") if c.strip()]

    if "rating_level" not in prof:
        lvl = prof.get("level")
        prof["rating_level"] = (
            "national" if lvl == "senior" else ("provincial" if lvl == "intermediate" else "local")
        )

    return prof


def _split_list(v):
    if not v:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return [x.strip() for x in str(v).replace("，", ",").split(",") if x.strip()]


def _extract_region(info: dict):
    def _get(*keys):
        for k in keys:
            if k in info and info[k]:
                return str(info[k])
        return ""

    prov = _get("省", "省份", "所在省", "省/直辖市", "省份/直辖市", "所属省份")
    city = _get("市", "城市", "所在市", "市/州", "地区", "地市", "所在地市", "所在地区")
    dist = _get("区县", "县", "区", "所在区县")

    def _norm(x):
        if not x:
            return ""
        s = str(x).strip()
        for suf in ["省", "市", "自治区", "地区", "区", "县"]:
            s = s.replace(suf, "")
        return s

    return _norm(prov), _norm(city), _norm(dist)


def _in_scope(ent_info: dict, profile: dict) -> bool:
    """根据专家评级等级与地域范围，判断企业是否在服务范围内"""
    level = (profile.get("rating_level") or "local").lower()
    prov, city, dist = _extract_region(ent_info or {})

    pprov_list = _split_list(profile.get("province"))
    pcity_list = _split_list(profile.get("city"))
    pdist_list = _split_list(profile.get("district"))

    # 国家级：不限制
    if level == "national":
        return True

    # 省级：按省份过滤
    if level == "provincial":
        if not pprov_list:
            return True
        if not prov:
            return True
        return any(pp in prov for pp in pprov_list)

    # 地市级：优先看省，其次看市/区
    if not pprov_list and not pcity_list:
        return True

    if pprov_list and prov and not any(pp in prov for pp in pprov_list):
        return False

    if pcity_list:
        if not city:
            return True
        if not any(pc in city for pc in pcity_list):
            return False

    if pdist_list:
        if dist and not any(pd in dist for pd in pdist_list):
            return False

    return True


# ============== 企业数据聚合 ==============
def _iter_enterprises(limit=300):
    base = current_app.config.get("SUBMISSIONS_FOLDER", SUBMISSION_DIR)
    if not os.path.exists(base):
        return []

    items = []
    for fn in os.listdir(base):
        if not fn.endswith(".json") or not fn.startswith("submission_"):
            continue
        jp = os.path.join(base, fn)
        try:
            mtime = os.path.getmtime(jp)
        except Exception:
            continue
        items.append((mtime, jp))

    items.sort(reverse=True)
    items = items[:limit]

    result = []
    for _, jp in items:
        try:
            with open(jp, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        info = data.get("enterprise_info") or {}
        username = data.get("username") or ""
        level = data.get("user_level") or "beginner"

        xlsx = jp.replace("submission_", "问卷_").replace(".json", ".xlsx")
        score = {}
        if os.path.exists(xlsx):
            score = _compute_score_from_excel(xlsx)

        result.append(
            {
                "username": username or os.path.splitext(os.path.basename(jp))[0],
                "enterprise_name": info.get("企业名称", ""),
                "info": info,
                "user_level": level,
                "score": score,
                "submit_time": _ts_text(datetime.fromtimestamp(os.path.getmtime(jp)).isoformat(timespec="seconds")),
                "json_path": jp,
                "excel_path": xlsx if os.path.exists(xlsx) else None,
            }
        )

    return result


def _latest_by_username():
    """按企业账号聚合，只保留最新一次提交"""
    latest = {}
    for ent in _iter_enterprises():
        u = ent.get("username") or ent.get("enterprise_name")
        if not u:
            continue
        if u not in latest:
            latest[u] = ent
    return latest


# ============== 匹配概览 ==============
@api_bp.get("/matches")
def api_matches():
    """匹配概览：沿用原有匹配算法，并按地域范围过滤"""
    try:
        prof = _get_expert_profile()
        raw_items = get_expert_matches()

        # 需要企业地域信息做过滤
        ents_by_name = {e["enterprise_name"]: e for e in _iter_enterprises()}
        filtered = []
        for it in raw_items:
            ent = ents_by_name.get(it.get("enterprise_name") or "")
            if ent and not _in_scope(ent.get("info") or {}, prof):
                continue
            filtered.append(it)

        return jsonify({"success": True, "items": filtered, "profile": prof})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============== 首页统计 ==============
@api_bp.get("/stats")
def api_stats():
    """首页统计：企业数量、平均得分、等级分布、近30天台账与反馈"""
    prof = _get_expert_profile()
    latest_by_user = _latest_by_username()
    ents = list(latest_by_user.values())

    # 地域过滤
    ents = [e for e in ents if _in_scope(e.get("info") or {}, prof)]

    total = len(ents)
    scores = [float((e.get("score") or {}).get("percentage") or 0.0) for e in ents]
    avg_score = sum(scores) / len(scores) if scores else 0.0

    # 等级分布
    level_dist = {"beginner": 0, "intermediate": 0, "advanced": 0}
    for e in ents:
        lvl = e.get("user_level") or "beginner"
        if lvl not in level_dist:
            level_dist[lvl] = 0
        level_dist[lvl] += 1

    # 简单分数直方图
    buckets = [(0, 60), (60, 70), (70, 80), (80, 90), (90, 101)]
    hist = []
    for lo, hi in buckets:
        cnt = len([s for s in scores if lo <= s < hi])
        hist.append({"label": f"{lo}-{hi-1 if hi < 101 else 100}", "count": cnt})

    # 如果当前没有任何企业得分数据，为了保证首页可视化不空白，返回一组示意数据
    if not scores:
        level_dist = {"beginner": 3, "intermediate": 4, "advanced": 2}
        hist = [
            {"label": "0-59", "count": 1},
            {"label": "60-69", "count": 2},
            {"label": "70-79", "count": 3},
            {"label": "80-89", "count": 2},
            {"label": "90-100", "count": 1},
        ]

    # 台账 & 反馈统计
    uname = session.get("username") or "anonymous"
    ledgers = _load_json(os.path.join(LEDGER_DIR, f"{uname}.json"), [])
    feedbacks = _load_json(os.path.join(FEEDBACK_DIR, f"{uname}.json"), [])

    cutoff = datetime.utcnow() - timedelta(days=30)
    ledger_30 = []
    for l in ledgers:
        raw_ts = l.get("date") or l.get("created_at")
        try:
            if not raw_ts:
                continue
            dt = datetime.fromisoformat(str(raw_ts))
            if dt >= cutoff:
                ledger_30.append(l)
        except Exception:
            # 遇到格式不标准的旧数据时直接忽略，避免首页统计接口报错
            continue

    fb_submitted = len(feedbacks)
    fb_reviewed = len([f for f in feedbacks if f.get("status") == "reviewed"])

    return jsonify(
        {
            "success": True,
            "profile": prof,
            "enterprise_total": total,
            "level_distribution": level_dist,
            "avg_score": avg_score,
            "score_histogram": hist,
            "ledger_30_days": ledger_30,
            "feedback": {"submitted": fb_submitted, "reviewed": fb_reviewed},
        }
    )


# ============== 企业列表与详情 ==============
@api_bp.get("/enterprises")
def api_enterprises():
    """企业列表（已按专家地域范围过滤，可按名称关键字搜索）"""
    try:
        prof = _get_expert_profile()
        kw = (request.args.get("kw") or "").strip()

        ents = list(_latest_by_username().values())
        ents = [e for e in ents if _in_scope(e.get("info") or {}, prof)]

        if kw:
            ents = [e for e in ents if kw in (e.get("enterprise_name") or "")]

        items = []
        for e in ents:
            s = e.get("score") or {}
            items.append(
                {
                    "username": e.get("username"),
                    "enterprise_name": e.get("enterprise_name"),
                    "user_level": e.get("user_level"),
                    "score_percentage": float(s.get("percentage") or 0.0),
                    "submitted_at": e.get("submit_time"),
                }
            )

        return jsonify({"success": True, "items": items, "profile": prof})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.get("/enterprise/<username>")
def api_enterprise_detail(username):
    """单个企业详情（按账号筛最新一条）"""
    try:
        latest = _latest_by_username()
        ent = latest.get(username)
        if not ent:
            return jsonify({"success": False, "error": "未找到该企业"}), 404

        return jsonify(
            {
                "success": True,
                "enterprise_name": ent.get("enterprise_name"),
                "info": ent.get("info"),
                "user_level": ent.get("user_level"),
                "score": ent.get("score"),
                "excel_file": os.path.basename(ent.get("excel_path") or ""),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============== 辅导台账 ==============
def _ledger_file(username: str) -> str:
    return os.path.join(LEDGER_DIR, f"{username}.json")


@api_bp.get("/ledger")
def api_ledger_list():
    uname = session.get("username") or "anonymous"
    data = _load_json(_ledger_file(uname), [])
    return jsonify({"success": True, "items": data})


@api_bp.post("/ledger")
def api_ledger_save():
    uname = session.get("username") or "anonymous"
    payload = request.get_json(silent=True) or {}
    items = _load_json(_ledger_file(uname), [])

    rid = payload.get("id") or str(uuid.uuid4())
    now = _now_ts()

    # 更新或新增
    updated = False
    for it in items:
        if it.get("id") == rid:
            it.update(
                {
                    "enterprise_name": payload.get("enterprise_name", it.get("enterprise_name", "")),
                    "date": payload.get("date", it.get("date", now)),
                    "method": payload.get("method", it.get("method", "")),
                    "summary": payload.get("summary", it.get("summary", "")),
                    "next_plan": payload.get("next_plan", it.get("next_plan", "")),
                    "updated_at": now,
                }
            )
            updated = True
            break

    if not updated:
        items.append(
            {
                "id": rid,
                "enterprise_name": payload.get("enterprise_name", ""),
                "date": payload.get("date") or now,
                "method": payload.get("method", ""),
                "summary": payload.get("summary", ""),
                "next_plan": payload.get("next_plan", ""),
                "created_at": now,
                "updated_at": now,
            }
        )

    _save_json(_ledger_file(uname), items)
    return jsonify({"success": True, "id": rid})


@api_bp.delete("/ledger/<rid>")
def api_ledger_delete(rid):
    uname = session.get("username") or "anonymous"
    items = _load_json(_ledger_file(uname), [])
    items = [it for it in items if it.get("id") != rid]
    _save_json(_ledger_file(uname), items)
    return jsonify({"success": True})


@api_bp.post("/ledger/<rid>/upload")
def api_ledger_upload(rid):
    """上传佐证材料（简单保存到 reports 目录，并在台账项中记录文件名）"""
    uname = session.get("username") or "anonymous"
    if "file" not in request.files:
        return jsonify({"success": False, "error": "缺少文件"}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"success": False, "error": "文件名为空"}), 400

    safe_name = secure_filename(f.filename)
    save_dir = os.path.join(REPORT_DIR, "ledger_attachments")
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"{rid}_{safe_name}")
    f.save(path)

    items = _load_json(_ledger_file(uname), [])
    for it in items:
        if it.get("id") == rid:
            files = it.get("attachments") or []
            files.append(os.path.basename(path))
            it["attachments"] = files
            break
    _save_json(_ledger_file(uname), items)

    return jsonify({"success": True, "filename": os.path.basename(path)})


# ============== 专项反馈 ==============
def _feedback_file(username: str) -> str:
    return os.path.join(FEEDBACK_DIR, f"{username}.json")


@api_bp.get("/feedback/my")
def api_feedback_my():
    uname = session.get("username") or "anonymous"
    data = _load_json(_feedback_file(uname), [])
    return jsonify({"success": True, "items": data})


@api_bp.post("/feedback")
def api_feedback_submit():
    uname = session.get("username") or "anonymous"
    payload = request.get_json(silent=True) or {}
    items = _load_json(_feedback_file(uname), [])

    fid = str(uuid.uuid4())
    now = _now_ts()
    item = {
        "id": fid,
        "title": payload.get("title", ""),
        "content": payload.get("content", ""),
        "scope": payload.get("scope", ""),
        "created_at": now,
        "status": "submitted",
    }
    items.append(item)
    _save_json(_feedback_file(uname), items)
    return jsonify({"success": True, "id": fid})


# ============== 我的信息 / 评级管理 ==============
@api_bp.get("/profile")
def api_profile_get():
    prof = _get_expert_profile()
    return jsonify({"success": True, "profile": prof})


@api_bp.post("/profile")
def api_profile_save():
    uname = session.get("username") or "anonymous"
    payload = request.get_json(silent=True) or {}
    prof = _get_expert_profile()

    for key in [
        "display_name",
        "email",
        "phone",
        "org",
        "title",
        "expertise",
        "bio",
        "rating_level",
        "province",
        "city",
        "district",
        "categories",
    ]:
        if key in payload:
            prof[key] = payload[key]

    # 保护评级字段
    if prof.get("rating_level") not in RATING_LEVELS:
        prof["rating_level"] = "local"

    _save_json(_profile_path(uname), prof)
    return jsonify({"success": True, "profile": prof})


# ============== 一键填充演示数据 ==============
@api_bp.post("/seed-demo")
def api_seed_demo():
    """为当前专家生成若干演示台账和专项反馈，方便展示界面效果"""
    uname = session.get("username") or "anonymous"
    count = max(1, int((request.get_json(silent=True) or {}).get("count") or 5))

    ledgers = _load_json(_ledger_file(uname), [])
    feedbacks = _load_json(_feedback_file(uname), [])

    now = datetime.utcnow()
    sample_ents = [e.get("enterprise_name") for e in _iter_enterprises()[:5]] or ["示例企业A", "示例企业B"]

    # 生成台账
    for i in range(count):
        rid = str(uuid.uuid4())
        dt = (now - timedelta(days=i * 3)).isoformat(timespec="seconds")
        ledgers.append(
            {
                "id": rid,
                "enterprise_name": sample_ents[i % len(sample_ents)],
                "date": dt,
                "method": "线上+线下辅导",
                "summary": f"第{i+1}次辅导，围绕治理结构和合规管理开展诊断。",
                "next_plan": "下次围绕数字化能力提升开展辅导。",
                "created_at": dt,
                "updated_at": dt,
            }
        )

    # 生成反馈
    for i in range(count):
        fid = str(uuid.uuid4())
        dt = (now - timedelta(days=i * 5)).isoformat(timespec="seconds")
        feedbacks.append(
            {
                "id": fid,
                "title": f"关于第{i+1}轮辅导工作的建议",
                "content": "建议进一步加强与地方工商联的协同，优化问卷维度设置，增加数据导出功能。",
                "scope": "省级试点",
                "created_at": dt,
                "status": "submitted",
            }
        )

    _save_json(_ledger_file(uname), ledgers)
    _save_json(_feedback_file(uname), feedbacks)

    return jsonify(
        {
            "success": True,
            "message": "已为当前专家写入演示台账与反馈",
            "ledger_count": len(ledgers),
            "feedback_count": len(feedbacks),
        }
    )

