"""
email_service.py — Production-grade SMTP Email Delivery Service.
Handles HTML email templates and STARTTLS/SSL SMTP transmission for:
1. Email Verification
2. Password Reset
3. Interview Invitations
4. Application Status Updates

Tracks delivery logs (Pending, Sent, Failed) in PostgreSQL/SQLite database.
"""
import logging
import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.email_log import EmailLog

logger = logging.getLogger("ai_recruiter.email")


def _send_smtp_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str,
    email_type: str = "general",
    db: Optional[Session] = None,
) -> bool:
    """
    Helper method to log and transmit email via SMTP (port 587 + STARTTLS or SSL port 465).
    Persists delivery status (Pending -> Sent or Failed) to EmailLog table if db session provided.
    """
    email_log = None
    if db:
        try:
            email_log = EmailLog(
                to_email=to_email,
                subject=subject,
                email_type=email_type,
                status="Pending",
            )
            db.add(email_log)
            db.commit()
            db.refresh(email_log)
        except Exception as err:
            logger.error(f"Failed to create EmailLog record: {err}")

    smtp_user = settings.smtp_user_credential
    smtp_password = settings.SMTP_PASSWORD

    if not smtp_user or not smtp_password:
        logger.warning(
            "SMTP configuration missing: SMTP_USER / SMTP_USERNAME or SMTP_PASSWORD is not configured. Logging email to console."
        )
        print(f"\n==================== [DEV EMAIL DISPATCH: {email_type.upper()}] ====================")
        print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
        print(f"==============================================================\n")

        if db and email_log:
            try:
                email_log.status = "Sent"
                email_log.sent_at = datetime.now(timezone.utc)
                db.commit()
            except Exception:
                pass
        return True

    try:
        from_addr = settings.sender_email
        from_name = settings.sender_name

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
                server.login(smtp_user, smtp_password)
                server.sendmail(from_addr, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(from_addr, [to_email], msg.as_string())

        logger.info(f"Successfully delivered email via SMTP to {to_email}")
        print(f"✅ [SMTP SENT SUCCESS] Email delivered to {to_email}")

        if db and email_log:
            try:
                email_log.status = "Sent"
                email_log.sent_at = datetime.now(timezone.utc)
                db.commit()
            except Exception as e:
                logger.error(f"Failed to update EmailLog status: {e}")

        return True
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to send email via SMTP to {to_email}: {error_msg}")
        print(f"❌ [SMTP ERROR] Failed to send email to {to_email}: {error_msg}")

        if db and email_log:
            try:
                email_log.status = "Failed"
                email_log.error_message = error_msg
                db.commit()
            except Exception:
                pass

        return False


def send_verification_email(
    to_email: str, name: str, token: str, db: Optional[Session] = None, base_url: Optional[str] = None
) -> str:
    """Generates and dispatches a secure Account Email Verification message."""
    url_base = base_url or settings.FRONTEND_URL or "http://localhost:8000"
    verify_url = f"{url_base.rstrip('/')}/verify-email.html?token={token}"
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
          <p>Thank you for registering with <strong>AI Recruiter Platform</strong>. To activate your account and access your dashboard, please verify your email address below.</p>
          
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

Thank you for registering with AI Recruiter Platform.
To activate your account, please verify your email address by visiting the link below:

{verify_url}

Note: This link is single-use and expires in 24 hours.
If you did not create an account, please ignore this email.
    """

    _send_smtp_email(to_email, subject, html_content, text_content, email_type="verification", db=db)
    return verify_url


def send_reset_password_email(
    to_email: str, name: str, token: str, db: Optional[Session] = None, base_url: Optional[str] = None
) -> str:
    """Generates and dispatches a secure Password Reset message."""
    url_base = base_url or settings.FRONTEND_URL or "http://localhost:8000"
    reset_url = f"{url_base.rstrip('/')}/reset-password.html?token={token}"
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
          <p>We received a request to reset the password for your <strong>AI Recruiter</strong> account. Click the button below to set a new password:</p>
          
          <div style="text-align: center;">
            <a href="{reset_url}" class="btn">Reset My Password &rarr;</a>
          </div>

          <p style="font-size: 13px; color: #64748b;">Or copy and paste this link into your web browser:</p>
          <div class="link-box"><a href="{reset_url}" style="color: #dc2626;">{reset_url}</a></div>

          <div class="warning">
            🔒 <strong>Security Notice:</strong> This link is single-use and valid for <strong>30 minutes</strong>. If you did not request a password reset, please ignore this message.
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

    _send_smtp_email(to_email, subject, html_content, text_content, email_type="password_reset", db=db)
    return reset_url


def send_interview_invitation_email(
    to_email: str,
    candidate_name: str,
    company_name: str,
    job_title: str,
    interview_date: str,
    interview_time: str,
    location_or_link: str,
    instructions: str = "Please make sure you have a working camera, microphone, and stable internet connection.",
    db: Optional[Session] = None,
) -> bool:
    """Sends a formatted, professional interview invitation email to a candidate."""
    subject = f"Interview Invitation: {job_title} at {company_name}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
        .header {{ background: linear-gradient(135deg, #0d9488 0%, #0284c7 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; font-weight: 700; }}
        .badge {{ display: inline-block; background-color: rgba(255,255,255,0.2); color: #ffffff; font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 9999px; margin-top: 8px; }}
        .content {{ padding: 32px 28px; color: #334155; line-height: 1.6; }}
        .details-card {{ background-color: #f1f5f9; border-left: 4px solid #0284c7; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .detail-row {{ margin-bottom: 10px; font-size: 14px; }}
        .detail-label {{ font-weight: 700; color: #1e293b; width: 140px; display: inline-block; }}
        .btn {{ display: inline-block; background-color: #0284c7; color: #ffffff !important; padding: 14px 32px; text-decoration: none; font-weight: 600; font-size: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }}
        .instructions-box {{ background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 16px; font-size: 13px; color: #92400e; margin-top: 20px; }}
        .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>📅 Interview Invitation</h1>
          <div class="badge">{company_name}</div>
        </div>
        <div class="content">
          <p style="font-size: 16px; font-weight: 600; color: #0f172a;">Dear {candidate_name},</p>
          <p>We are pleased to invite you for an interview for the <strong>{job_title}</strong> position at <strong>{company_name}</strong>.</p>
          
          <div class="details-card">
            <div class="detail-row"><span class="detail-label">Candidate Name:</span> {candidate_name}</div>
            <div class="detail-row"><span class="detail-label">Company Name:</span> {company_name}</div>
            <div class="detail-row"><span class="detail-label">Job Title:</span> {job_title}</div>
            <div class="detail-row"><span class="detail-label">Scheduled Date:</span> {interview_date}</div>
            <div class="detail-row"><span class="detail-label">Scheduled Time:</span> {interview_time}</div>
            <div class="detail-row"><span class="detail-label">Interview Meeting:</span> <a href="{location_or_link}" style="color: #0284c7; font-weight: 600;">Join Meeting / Access Portal</a></div>
          </div>

          <div style="text-align: center;">
            <a href="{location_or_link}" class="btn">Start / Join Interview &rarr;</a>
          </div>

          <div class="instructions-box">
            💡 <strong>Interview Instructions:</strong> {instructions}
          </div>

          <p style="font-size: 13px; color: #64748b; margin-top: 24px;">
            If you need to reschedule or have any questions prior to the interview, please respond directly to this email or contact the recruiter.
          </p>
        </div>
        <div class="footer">
          &copy; {company_name} via AI Recruiter Platform &bull; Automated Candidate System
        </div>
      </div>
    </body>
    </html>
    """

    text_content = f"""
Dear {candidate_name},

We are pleased to invite you for an interview for the {job_title} position at {company_name}.

Interview Details:
------------------
Candidate Name: {candidate_name}
Company Name:   {company_name}
Job Title:      {job_title}
Date:           {interview_date}
Time:           {interview_time}
Link / Location: {location_or_link}

Instructions:
{instructions}

Please visit the link above to access your interview session.
    """

    return _send_smtp_email(to_email, subject, html_content, text_content, email_type="interview_invitation", db=db)


def send_application_status_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    new_status: str,
    notes: Optional[str] = None,
    db: Optional[Session] = None,
) -> bool:
    """Sends a candidate notification email whenever their job application status updates."""
    clean_status = new_status.replace("_", " ").title()
    subject = f"Application Update: {job_title} at {company_name}"

    status_color_map = {
        "Applied": "#3b82f6",
        "Under Review": "#8b5cf6",
        "Shortlisted": "#10b981",
        "Interview Scheduled": "#0284c7",
        "Selected": "#16a34a",
        "Rejected": "#ef4444",
    }
    badge_color = status_color_map.get(clean_status, "#2563eb")

    status_messages = {
        "Applied": "Your application has been received and logged successfully.",
        "Under Review": "Our talent acquisition team is actively reviewing your application and candidate profile.",
        "Shortlisted": "Great news! Your application has been shortlisted for further evaluation.",
        "Interview Scheduled": "You have been selected for an interview session. Details have been updated in your portal.",
        "Selected": "Congratulations! We are delighted to inform you that you have been selected for this role.",
        "Rejected": "Thank you for your interest in joining our team. While we were impressed with your background, we have decided to move forward with other candidates at this time.",
    }
    status_desc = status_messages.get(clean_status, f"Your application status is now updated to {clean_status}.")

    portal_url = f"{settings.FRONTEND_URL.rstrip('/')}/my-applications.html"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
        .header {{ background: linear-gradient(135deg, #1e293b 0%, #334155 100%); color: #ffffff; padding: 32px 24px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 22px; font-weight: 700; }}
        .content {{ padding: 32px 28px; color: #334155; line-height: 1.6; }}
        .status-badge {{ display: inline-block; background-color: {badge_color}; color: #ffffff; font-size: 15px; font-weight: 700; padding: 10px 24px; border-radius: 9999px; margin: 16px 0; }}
        .details-box {{ background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 8px; margin: 20px 0; font-size: 14px; }}
        .btn {{ display: inline-block; background-color: #2563eb; color: #ffffff !important; padding: 12px 28px; text-decoration: none; font-weight: 600; font-size: 14px; border-radius: 8px; margin-top: 16px; text-align: center; }}
        .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>📋 Application Status Update</h1>
          <div style="font-size: 13px; opacity: 0.9; margin-top: 4px;">{company_name}</div>
        </div>
        <div class="content">
          <p style="font-size: 16px; font-weight: 600; color: #0f172a;">Hello {candidate_name},</p>
          <p>There is an update on your application for the <strong>{job_title}</strong> position at <strong>{company_name}</strong>.</p>
          
          <div style="text-align: center;">
            <div class="status-badge">Current Status: {clean_status}</div>
          </div>

          <div class="details-box">
            <p style="margin: 0; font-weight: 600; color: #1e293b;">Details / Next Steps:</p>
            <p style="margin: 8px 0 0 0; color: #475569;">{status_desc}</p>
            {f'<p style="margin-top: 12px; font-size: 13px; color: #64748b; font-style: italic;">Recruiter Note: {notes}</p>' if notes else ''}
          </div>

          <div style="text-align: center;">
            <a href="{portal_url}" class="btn">View Application Portal &rarr;</a>
          </div>
        </div>
        <div class="footer">
          &copy; {company_name} &bull; Powered by AI Recruiter Platform
        </div>
      </div>
    </body>
    </html>
    """

    text_content = f"""
Hello {candidate_name},

Your application status for {job_title} at {company_name} has been updated.

New Status: {clean_status}

{status_desc}
{f"Recruiter Note: {notes}" if notes else ""}

View your candidate portal at: {portal_url}
    """

    return _send_smtp_email(to_email, subject, html_content, text_content, email_type="status_update", db=db)
