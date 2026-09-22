"""
Pydantic schemas for chat and messaging.
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    receiver_id: uuid.UUID
    content: Optional[str] = None
    application_id: Optional[uuid.UUID] = None
    is_audio: Optional[bool] = False
    audio_url: Optional[str] = None


class MessageUpdate(BaseModel):
    content: Optional[str] = None


class MessageResponse(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    sender_name: str
    sender_role: str
    receiver_id: uuid.UUID
    receiver_name: str
    receiver_role: str
    application_id: Optional[uuid.UUID] = None
    content: Optional[str] = None
    is_audio: bool = False
    audio_url: Optional[str] = None
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactResponse(BaseModel):
    user_id: uuid.UUID
    name: str
    email: str
    role: str
    company_or_headline: Optional[str] = None
    application_id: Optional[uuid.UUID] = None
    job_title: Optional[str] = None


class ConversationResponse(BaseModel):
    other_user_id: uuid.UUID
    other_user_name: str
    other_user_role: str
    other_user_email: str
    company_or_headline: Optional[str] = None
    last_message: Optional[str] = None
    last_message_is_audio: bool = False
    last_message_at: datetime
    unread_count: int
    application_id: Optional[uuid.UUID] = None


class UnreadCountResponse(BaseModel):
    unread_count: int
