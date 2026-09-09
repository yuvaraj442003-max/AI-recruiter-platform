"""
ics_service.py — Dynamic RFC 5545 iCalendar (.ics) File Generator.
Produces standard .ics calendar invite content compatible with Google Calendar,
Outlook, Apple Calendar, and iCal.
"""
from datetime import datetime, timezone
from typing import Optional


def generate_ics_content(
    summary: str,
    description: str,
    start_time_utc: datetime,
    end_time_utc: datetime,
    location_or_url: str = "",
    organizer_email: str = "noreply@airecruiter.com",
    organizer_name: str = "AI Recruiter",
    attendee_email: Optional[str] = None,
    attendee_name: Optional[str] = None,
    uid: Optional[str] = None,
) -> str:
    """
    Generates a valid iCalendar (.ics) string.
    """
    fmt = "%Y%m%dT%H%M%SZ"
    dtstamp = datetime.now(timezone.utc).strftime(fmt)
    dtstart = start_time_utc.strftime(fmt) if start_time_utc.tzinfo else start_time_utc.replace(tzinfo=timezone.utc).strftime(fmt)
    dtend = end_time_utc.strftime(fmt) if end_time_utc.tzinfo else end_time_utc.replace(tzinfo=timezone.utc).strftime(fmt)

    event_uid = uid or f"interview_{dtstart}_{start_time_utc.timestamp()}@airecruiter.com"

    # Clean description string for ICS formatting (escape newlines and special characters)
    clean_desc = description.replace("\r", "").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")
    clean_summary = summary.replace(",", "\\,").replace(";", "\\;")

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Recruiter Platform//Interview Calendar 1.0//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:REQUEST",
        "BEGIN:VEVENT",
        f"UID:{event_uid}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"SUMMARY:{clean_summary}",
        f"DESCRIPTION:{clean_desc}",
    ]

    if location_or_url:
        clean_loc = location_or_url.replace(",", "\\,").replace(";", "\\;")
        lines.append(f"LOCATION:{clean_loc}")
        lines.append(f"URL:{location_or_url}")

    lines.append(f"ORGANIZER;CN={organizer_name}:mailto:{organizer_email}")

    if attendee_email:
        att_name = attendee_name or attendee_email
        lines.append(f"ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN={att_name}:mailto:{attendee_email}")

    lines.extend([
        "STATUS:CONFIRMED",
        "SEQUENCE:0",
        "BEGIN:VALARM",
        "TRIGGER:-PT15M",
        "ACTION:DISPLAY",
        "DESCRIPTION:Interview Reminder",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR",
    ])

    return "\r\n".join(lines)
