"""
email_service.py — Production-grade Gmail SMTP Email Delivery Service.
Handles HTML email templates and STARTTLS SMTP transmission for Email Verification and Password Reset.
"""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings
from app.core.exceptions import AppError

logger = logging.getLogger("ai_recruiter.email")


def _send_smtp_email(to_email: str, subject: str, html_content: str, text_content: str) -> bool:
    """Helper method to transmit email via Gmail SMTP (port 587 + STARTTLS) or SSL (port 465)."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP configuration missing: SMTP_USER or SMTP_PASSWORD is not set in backend/.env. Logging email to console.")
        print(f"\n==================== [DEV EMAIL DISPATCH] ====================")
        print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
        print(f"==============================================================\n")
        return False

    try:
        from_addr = settings.EMAILS_FROM_EMAIL or settings.SMTP_USER
        from_name = settings.EMAILS_FROM_NAME or "AI Recruiter Team"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{from_name} <{from_addr}>"
        msg["To"] = to_email

        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)

        smtp_host = settings.SMTP_HOST or "smtp.gmail.com"
        smtp_port = int(settings.SMTP_PORT or 587)

        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(from_addr, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(from_addr, [to_email], msg.as_string())

        logger.info(f"Successfully delivered email via SMTP to {to_email}")
        print(f"✅ [SMTP SENT SUCCESS] Email delivered to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email via SMTP to {to_email}: {e}")
        print(f"❌ [SMTP ERROR] Failed to send email to {to_email}: {e}")
        return False


def send_verification_email(to_email: str, name: str, token: str, base_url: str = "http://localhost:8000") -> str:
    """Generates and dispatches a secure Account Email Verification message."""
    verify_url = f"{base_url.rstrip('/')}/verify-email.html?token={token}"
    subject = "Verify Your AI Recruiter Account"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
        .header {{ background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.5px; }}
        .content {{ padding: 32px 28px; color: #334155; line-height: 1.6; }}
        .btn {{ display: inline-block; background-color: #2563eb; color: #ffffff !important; padding: 14px 32px; text-decoration: none; font-weight: 600; font-size: 15px; border-radius: 8px; margin: 24px 0; text-align: center; }}
        .link-box {{ background-color: #f1f5f9; padding: 12px 16px; border-radius: 6px; font-size: 13px; color: #475569; word-break: break-all; margin-top: 16px; }}
        .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
        .badge {{ display: inline-block; background-color: #dbeafe; color: #1e40af; font-size: 12px; font-weight: 600; padding: 4px 10px; border-radius: 9999px; margin-top: 8px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>⚡ AI Recruiter Platform</h1>
          <div class="badge">Account Security Verification</div>
        </div>
        <div class="content">
          <p style="font-size: 16px; font-weight: 600; color: #0f172a;">Hello {name},</p>
          <p>Thank you for creating an account with <strong>AI Recruiter Platform</strong>. To activate your account and start using our intelligent ATS resume matching and AI recruitment services, please verify your email address.</p>
          
          <div style="text-align: center;">
            <a href="{verify_url}" class="btn">Verify My Account &rarr;</a>
          </div>

          <p style="font-size: 13px; color: #64748b;">Or copy and paste this secure link into your web browser:</p>
          <div class="link-box"><a href="{verify_url}" style="color: #2563eb;">{verify_url}</a></div>

          <p style="font-size: 13px; color: #e11d48; margin-top: 24px; font-weight: 600;">
            ⏳ Note: This verification link is single-use and will expire in 24 hours.
          </p>
          <p style="font-size: 12px; color: #64748b;">If you did not register for an account on AI Recruiter, please ignore this email.</p>
        </div>
        <div class="footer">
          &copy; AI Recruiter Platform &bull; Secure Authentication System
        </div>
      </div>
    </body>
    </html>
    """

    text_content = f"""
Hello {name},

Thank you for creating an account with AI Recruiter Platform.
To activate your account, please verify your email address by visiting the link below:

{verify_url}

Note: This link is single-use and expires in 24 hours.
If you did not create an account, please ignore this email.
    """

    _send_smtp_email(to_email, subject, html_content, text_content)
    return verify_url


def send_reset_password_email(to_email: str, name: str, token: str, base_url: str = "http://localhost:8000") -> str:
    """Generates and dispatches a secure Password Reset message."""
    reset_url = f"{base_url.rstrip('/')}/reset-password.html?token={token}"
    subject = "Reset Your AI Recruiter Password"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
        .header {{ background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; font-weight: 700; }}
        .content {{ padding: 32px 28px; color: #334155; line-height: 1.6; }}
        .btn {{ display: inline-block; background-color: #dc2626; color: #ffffff !important; padding: 14px 32px; text-decoration: none; font-weight: 600; font-size: 15px; border-radius: 8px; margin: 24px 0; text-align: center; }}
        .link-box {{ background-color: #f1f5f9; padding: 12px 16px; border-radius: 6px; font-size: 13px; color: #475569; word-break: break-all; margin-top: 16px; }}
        .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
        .warning {{ background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; font-size: 13px; color: #991b1b; border-radius: 4px; margin-top: 20px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>⚡ AI Recruiter Platform</h1>
          <div style="font-size: 13px; opacity: 0.9;">Password Reset Request</div>
        </div>
        <div class="content">
          <p style="font-size: 16px; font-weight: 600; color: #0f172a;">Hello {name},</p>
          <p>We received a request to reset your password for your <strong>AI Recruiter</strong> account. Click the button below to choose a new password:</p>
          
          <div style="text-align: center;">
            <a href="{reset_url}" class="btn">Reset My Password &rarr;</a>
          </div>

          <p style="font-size: 13px; color: #64748b;">Or copy and paste this link into your web browser:</p>
          <div class="link-box"><a href="{reset_url}" style="color: #dc2626;">{reset_url}</a></div>

          <div class="warning">
            🔒 <strong>Security Notice:</strong> This link is single-use and valid for <strong>30 minutes</strong>. If you did not request a password reset, please ignore this message or contact support immediately.
          </div>
        </div>
        <div class="footer">
          &copy; AI Recruiter Platform &bull; Account Security System
        </div>
      </div>
    </body>
    </html>
    """

    text_content = f"""
Hello {name},

We received a request to reset your password for your AI Recruiter account.
Please visit the following link within 30 minutes to set a new password:

{reset_url}

If you did not request a password reset, you can safely ignore this email.
    """

    _send_smtp_email(to_email, subject, html_content, text_content)
    return reset_url
