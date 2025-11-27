"""
通知服务模块
实现邮件和短信发送功能
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr
import os
import json
import requests
from pathlib import Path


class NotificationService:
    """通知服务类"""

    def __init__(self, config_file='config.json'):
        """
        初始化通知服务

        Args:
            config_file: 配置文件路径
        """
        self.config = self._load_config(config_file)

    def _load_config(self, config_file):
        """加载配置文件"""
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 返回默认配置
            return {
                'email': {
                    'smtp_server': 'smtp.example.com',
                    'smtp_port': 587,
                    'username': 'your_email@example.com',
                    'password': 'your_password',
                    'from_name': '企业评价系统',
                    'use_tls': True
                },
                'sms': {
                    'provider': 'aliyun',  # 或 'tencent', 'twilio'
                    'access_key': 'your_access_key',
                    'access_secret': 'your_access_secret',
                    'sign_name': '企业评价系统',
                    'template_code': 'SMS_12345678'
                }
            }

    def send_email(self, to_email, enterprise_name, contact_name,
                   report_url, attachment_path=None):
        """
        发送邮件通知

        Args:
            to_email: 收件人邮箱
            enterprise_name: 企业名称
            contact_name: 联系人姓名
            report_url: 报告下载链接
            attachment_path: 附件路径(可选)

        Returns:
            bool: 发送是否成功
        """
        try:
            email_config = self.config.get('email', {})

            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = formataddr((
                email_config.get('from_name', '企业评价系统'),
                email_config.get('username')
            ))
            msg['To'] = to_email
            msg['Subject'] = Header(
                f'{enterprise_name} - 现代企业制度评价自评报告',
                'utf-8'
            )

            # 邮件正文
            html_content = self._generate_email_html(
                enterprise_name,
                contact_name,
                report_url
            )

            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            # 添加附件
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    attachment = MIMEApplication(f.read())
                    filename = os.path.basename(attachment_path)
                    attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=('utf-8', '', filename)
                    )
                    msg.attach(attachment)

            # 发送邮件
            smtp_server = email_config.get('smtp_server')
            smtp_port = email_config.get('smtp_port', 587)
            username = email_config.get('username')
            password = email_config.get('password')
            use_tls = email_config.get('use_tls', True)

            if use_tls:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)

            server.login(username, password)
            server.send_message(msg)
            server.quit()

            print(f"邮件发送成功: {to_email}")
            return True

        except Exception as e:
            print(f"邮件发送失败: {to_email}, 错误: {str(e)}")
            return False

    def _generate_email_html(self, enterprise_name, contact_name, report_url):
        """
        生成邮件HTML内容
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: "Microsoft YaHei", Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border: 1px solid #ddd;
                }}
                .button {{
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    background: #f0f0f0;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                    border-radius: 0 0 10px 10px;
                }}
                .info-box {{
                    background: white;
                    padding: 15px;
                    border-left: 4px solid #667eea;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>中国特色现代企业制度评价</h1>
                <p>企业自评报告已生成</p>
            </div>

            <div class="content">
                <p>尊敬的 {contact_name} 先生/女士,</p>

                <p>您好!</p>

                <p><strong>{enterprise_name}</strong> 的现代企业制度评价自评报告已生成完毕。</p>

                <div class="info-box">
                    <h3>📊 报告内容包括:</h3>
                    <ul>
                        <li>企业基本信息</li>
                        <li>评价指标自评</li>
                        <li>评分汇总与分析</li>
                        <li>评价结论</li>
                        <li>改进建议</li>
                    </ul>
                </div>

                <p>您可以通过以下方式查看报告:</p>

                <div style="text-align: center;">
                    <a href="{report_url}" class="button">📥 点击下载报告</a>
                </div>

                <p style="margin-top: 20px; font-size: 14px; color: #666;">
                    或复制以下链接到浏览器打开:<br>
                    <code>{report_url}</code>
                </p>

                <div class="info-box">
                    <p><strong>📌 温馨提示:</strong></p>
                    <ul>
                        <li>请妥善保存此报告</li>
                        <li>如有疑问请及时联系我们</li>
                        <li>报告链接7天内有效</li>
                    </ul>
                </div>
            </div>

            <div class="footer">
                <p>此邮件为系统自动发送,请勿直接回复</p>
                <p>© 2025 企业现代制度评价系统</p>
            </div>
        </body>
        </html>
        """
        return html

    def send_sms(self, phone, enterprise_name, report_url):
        """
        发送短信通知

        Args:
            phone: 手机号码
            enterprise_name: 企业名称
            report_url: 报告链接

        Returns:
            bool: 发送是否成功
        """
        try:
            sms_config = self.config.get('sms', {})
            provider = sms_config.get('provider', 'aliyun')

            # 短信内容
            message = f"【{sms_config.get('sign_name', '企业评价系统')}】{enterprise_name}的现代企业制度评价报告已生成,请访问 {report_url} 查看下载。"

            if provider == 'aliyun':
                return self._send_aliyun_sms(phone, sms_config, message)
            elif provider == 'tencent':
                return self._send_tencent_sms(phone, sms_config, message)
            elif provider == 'twilio':
                return self._send_twilio_sms(phone, sms_config, message)
            else:
                print(f"不支持的短信服务商: {provider}")
                return False

        except Exception as e:
            print(f"短信发送失败: {phone}, 错误: {str(e)}")
            return False

    def _send_aliyun_sms(self, phone, config, message):
        """
        通过阿里云发送短信
        需要安装: pip install aliyun-python-sdk-core
        """
        try:
            from aliyunsdkcore.client import AcsClient
            from aliyunsdkcore.request import CommonRequest

            client = AcsClient(
                config.get('access_key'),
                config.get('access_secret'),
                'cn-hangzhou'
            )

            request = CommonRequest()
            request.set_accept_format('json')
            request.set_domain('dysmsapi.aliyuncs.com')
            request.set_method('POST')
            request.set_protocol_type('https')
            request.set_version('2017-05-25')
            request.set_action_name('SendSms')

            request.add_query_param('PhoneNumbers', phone)
            request.add_query_param('SignName', config.get('sign_name'))
            request.add_query_param('TemplateCode', config.get('template_code'))
            request.add_query_param('TemplateParam', json.dumps({
                'enterprise': message
            }))

            response = client.do_action_with_exception(request)
            print(f"阿里云短信发送成功: {phone}")
            return True

        except ImportError:
            print("请安装阿里云SDK: pip install aliyun-python-sdk-core")
            return False
        except Exception as e:
            print(f"阿里云短信发送失败: {str(e)}")
            return False

    def _send_tencent_sms(self, phone, config, message):
        """
        通过腾讯云发送短信
        需要安装: pip install tencentcloud-sdk-python
        """
        try:
            from tencentcloud.common import credential
            from tencentcloud.sms.v20210111 import sms_client, models

            cred = credential.Credential(
                config.get('access_key'),
                config.get('access_secret')
            )

            client = sms_client.SmsClient(cred, "ap-guangzhou")
            req = models.SendSmsRequest()

            req.SmsSdkAppId = config.get('app_id')
            req.SignName = config.get('sign_name')
            req.TemplateId = config.get('template_code')
            req.PhoneNumberSet = [phone]
            req.TemplateParamSet = [message]

            resp = client.SendSms(req)
            print(f"腾讯云短信发送成功: {phone}")
            return True

        except ImportError:
            print("请安装腾讯云SDK: pip install tencentcloud-sdk-python")
            return False
        except Exception as e:
            print(f"腾讯云短信发送失败: {str(e)}")
            return False

    def _send_twilio_sms(self, phone, config, message):
        """
        通过Twilio发送短信(国际短信)
        需要安装: pip install twilio
        """
        try:
            from twilio.rest import Client

            client = Client(
                config.get('account_sid'),
                config.get('auth_token')
            )

            message = client.messages.create(
                body=message,
                from_=config.get('from_number'),
                to=phone
            )

            print(f"Twilio短信发送成功: {phone}")
            return True

        except ImportError:
            print("请安装Twilio SDK: pip install twilio")
            return False
        except Exception as e:
            print(f"Twilio短信发送失败: {str(e)}")
            return False

    def send_test_email(self, to_email):
        """
        发送测试邮件

        Args:
            to_email: 收件人邮箱

        Returns:
            bool: 发送是否成功
        """
        return self.send_email(
            to_email=to_email,
            enterprise_name='测试企业',
            contact_name='测试用户',
            report_url='http://example.com/test'
        )

    def send_test_sms(self, phone):
        """
        发送测试短信

        Args:
            phone: 手机号码

        Returns:
            bool: 发送是否成功
        """
        return self.send_sms(
            phone=phone,
            enterprise_name='测试企业',
            report_url='http://example.com/test'
        )
