"""
portfolio.py — Pydantic Schemas for Candidate Portfolio Builder & Public Portfolios.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ExperienceItem(BaseModel):
    title: str = ""
    company: str = ""
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None
    highlights: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)


class EducationItem(BaseModel):
    degree: str = ""
    institution: str = ""
    field_of_study: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    grade: Optional[str] = None
    activities: Optional[str] = None


class ProjectItem(BaseModel):
    name: str = ""
    description: str = ""
    contribution: Optional[str] = None
    technologies: list[str] = Field(default_factory=list)
    key_features: list[str] = Field(default_factory=list)
    live_demo_url: Optional[str] = None
    github_url: Optional[str] = None
    image_url: Optional[str] = None


class CertificationItem(BaseModel):
    name: str = ""
    organization: Optional[str] = None
    year: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class AchievementItem(BaseModel):
    title: str = ""
    description: Optional[str] = None
    year: Optional[str] = None
    organization: Optional[str] = None


class ServiceItem(BaseModel):
    title: str = ""
    description: str = ""
    icon: Optional[str] = "⚡"


class SocialLinks(BaseModel):
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None


class PortfolioCreateRequest(BaseModel):
    use_existing_resume: bool = True
    theme_id: Optional[str] = "modern"


class PromptGenerateRequest(BaseModel):
    prompt: str
    include_resume: bool = True
    refinement: bool = False


class RefineSectionRequest(BaseModel):
    section: str
    instruction: str


class PortfolioUpdateRequest(BaseModel):
    slug: Optional[str] = None
    theme_id: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    font: Optional[str] = None
    background_style: Optional[str] = None
    background_image: Optional[str] = None
    dark_mode: Optional[bool] = None
    button_style: Optional[str] = None
    card_style: Optional[str] = None
    layout: Optional[str] = None
    profile_image: Optional[str] = None
    professional_headline: Optional[str] = None
    headline_options: Optional[list[str]] = None
    about: Optional[str] = None
    skills: Optional[Union[Dict[str, list[str]], list[str], str]] = None
    experience: Optional[list[Dict[str, Any]]] = None
    education: Optional[list[Dict[str, Any]]] = None
    projects: Optional[list[Dict[str, Any]]] = None
    certifications: Optional[list[Dict[str, Any]]] = None
    achievements: Optional[list[Dict[str, Any]]] = None
    services: Optional[list[Dict[str, Any]]] = None
    social_links: Optional[Dict[str, Any]] = None
    candidate_name: Optional[str] = None
    section_order: Optional[list[str]] = None
    section_visibility: Optional[Dict[str, bool]] = None
    custom_css: Optional[str] = None


class PortfolioThemeUpdateRequest(BaseModel):
    theme_id: str


class PortfolioCustomizeUpdateRequest(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    font: Optional[str] = None
    background_style: Optional[str] = None
    background_image: Optional[str] = None
    dark_mode: Optional[bool] = None
    button_style: Optional[str] = None
    card_style: Optional[str] = None
    layout: Optional[str] = None
    section_order: Optional[list[str]] = None
    section_visibility: Optional[Dict[str, bool]] = None


class HeadlineGenerateRequest(BaseModel):
    current_role: Optional[str] = None
    key_skills: Optional[list[str]] = None


class HeadlineGenerateResponse(BaseModel):
    headlines: list[str]


class ImproveAboutRequest(BaseModel):
    about_text: Optional[str] = None
    tone: Optional[str] = "professional"  # professional, executive, creative, technical


class ImproveAboutResponse(BaseModel):
    improved_about: str
    original_about: Optional[str] = None
    tone: str


class ImproveExperienceRequest(BaseModel):
    experience_item: Dict[str, Any]


class ImproveExperienceResponse(BaseModel):
    improved_experience: Dict[str, Any]
    original_experience: Dict[str, Any]


class ImproveProjectRequest(BaseModel):
    project_item: Dict[str, Any]


class ImproveProjectResponse(BaseModel):
    improved_project: Dict[str, Any]
    original_project: Dict[str, Any]


class OrganizeSkillsRequest(BaseModel):
    skills: Optional[Union[list[str], Dict[str, Any], str]] = None


class OrganizeSkillsResponse(BaseModel):
    categorized_skills: Dict[str, list[str]]


class CheckSlugResponse(BaseModel):
    slug: str
    is_available: bool
    message: str


class PortfolioResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    candidate_name: str
    candidate_email: Optional[str] = None
    slug: str
    is_published: bool
    views_count: int
    theme_id: str
    primary_color: str
    secondary_color: str
    font: str
    background_style: str
    background_image: Optional[str] = None
    dark_mode: bool
    button_style: str
    card_style: str
    layout: str
    profile_image: Optional[str] = None
    professional_headline: Optional[str] = None
    headline_options: list[str] = Field(default_factory=list)
    about: Optional[str] = None
    skills: Any = None
    experience: list[Dict[str, Any]] = Field(default_factory=list)
    education: list[Dict[str, Any]] = Field(default_factory=list)
    projects: list[Dict[str, Any]] = Field(default_factory=list)
    certifications: list[Dict[str, Any]] = Field(default_factory=list)
    achievements: list[Dict[str, Any]] = Field(default_factory=list)
    services: list[Dict[str, Any]] = Field(default_factory=list)
    social_links: Dict[str, Any] = Field(default_factory=dict)
    section_order: list[str] = Field(default_factory=list)
    section_visibility: Dict[str, bool] = Field(default_factory=dict)
    custom_css: Optional[str] = None
    portrait_mask: Optional[str] = None
    public_url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PublicPortfolioResponse(BaseModel):
    candidate_name: str
    professional_headline: Optional[str] = None
    about: Optional[str] = None
    skills: Any = None
    experience: list[Dict[str, Any]] = Field(default_factory=list)
    education: list[Dict[str, Any]] = Field(default_factory=list)
    projects: list[Dict[str, Any]] = Field(default_factory=list)
    certifications: list[Dict[str, Any]] = Field(default_factory=list)
    achievements: list[Dict[str, Any]] = Field(default_factory=list)
    services: list[Dict[str, Any]] = Field(default_factory=list)
    social_links: Dict[str, Any] = Field(default_factory=dict)
    profile_image: Optional[str] = None
    theme_id: str
    primary_color: str
    secondary_color: str
    font: str
    background_style: str
    background_image: Optional[str] = None
    dark_mode: bool
    button_style: str
    card_style: str
    layout: str
    custom_css: Optional[str] = None
    portrait_mask: Optional[str] = None
    section_order: list[str] = Field(default_factory=list)
    section_visibility: Dict[str, bool] = Field(default_factory=dict)
    slug: str
    is_published: bool
    views_count: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
