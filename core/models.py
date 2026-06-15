"""
APEX — Core Pydantic Models
Strict data contracts shared across all agents and the LangGraph state.
Every agent reads from and writes to these schemas — no dict-passing anywhere.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────────────
# Resume Models
# ─────────────────────────────────────────────────────────────────────────────

class ContactInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""


class Experience(BaseModel):
    title: str = ""
    company: str = ""
    duration: str = ""
    bullets: List[str] = Field(default_factory=list)


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""
    gpa: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)
    bullets: List[str] = Field(default_factory=list)


class ParsedResume(BaseModel):
    contact: ContactInfo = Field(default_factory=ContactInfo)
    summary: str = ""
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    raw_text: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# Job Description Models
# ─────────────────────────────────────────────────────────────────────────────

class ParsedJobDescription(BaseModel):
    job_title: str = ""
    company: str = ""
    location: str = ""
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)
    soft_traits: List[str] = Field(default_factory=list)
    experience_years: str = ""
    technologies: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    raw_text: str = ""
    


# ─────────────────────────────────────────────────────────────────────────────
# ATS Analysis Models
# ─────────────────────────────────────────────────────────────────────────────

class SkillMatch(BaseModel):
    skill: str
    found_in_resume: bool
    importance: str = "required"  # "required" | "preferred"


class ATSResult(BaseModel):
    ats_score: int = 0                               # 0–100
    matched_skills: List[str] = Field(default_factory=list)
    missing_required_skills: List[str] = Field(default_factory=list)
    missing_preferred_skills: List[str] = Field(default_factory=list)
    keyword_coverage_pct: float = 0.0
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    skill_matches: List[SkillMatch] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Critique & Rewrite Models
# ─────────────────────────────────────────────────────────────────────────────

class BulletCritique(BaseModel):
    original: str
    issue: str        # What's wrong with this bullet
    suggestion: str   # How to fix it


class CritiqueResult(BaseModel):
    overall_assessment: str = ""
    weak_bullets: List[BulletCritique] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    missing_achievements: List[str] = Field(default_factory=list)
    structural_issues: List[str] = Field(default_factory=list)
    priority_fixes: List[str] = Field(default_factory=list)


class RewrittenBullet(BaseModel):
    original: str
    rewritten: str
    keywords_added: List[str] = Field(default_factory=list)


class RewriteResult(BaseModel):
    rewritten_summary: str = ""
    rewritten_bullets: List[RewrittenBullet] = Field(default_factory=list)
    keywords_injected: List[str] = Field(default_factory=list)
    new_ats_score_estimate: int = 0


# ─────────────────────────────────────────────────────────────────────────────
# Cover Letter Model
# ─────────────────────────────────────────────────────────────────────────────

class CoverLetter(BaseModel):
    subject_line: str = ""
    body: str = ""
    word_count: int = 0
    keywords_used: List[str] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Interview Models
# ─────────────────────────────────────────────────────────────────────────────

class InterviewQuestion(BaseModel):
    question: str
    category: str        # "hr" | "technical" | "behavioral" | "project"
    suggested_answer: str = ""
    tips: str = ""


class InterviewKit(BaseModel):
    hr_questions: List[InterviewQuestion] = Field(default_factory=list)
    technical_questions: List[InterviewQuestion] = Field(default_factory=list)
    behavioral_questions: List[InterviewQuestion] = Field(default_factory=list)
    project_questions: List[InterviewQuestion] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Learning Roadmap Model
# ─────────────────────────────────────────────────────────────────────────────

class LearningResource(BaseModel):
    skill: str
    resource_name: str
    resource_type: str   # "course" | "certification" | "project" | "documentation"
    platform: str
    estimated_time: str
    priority: str        # "high" | "medium" | "low"


class LearningRoadmap(BaseModel):
    skill_gaps: List[str] = Field(default_factory=list)
    quick_wins: List[str] = Field(default_factory=list)     # Can learn in < 1 week
    resources: List[LearningResource] = Field(default_factory=list)
    project_ideas: List[str] = Field(default_factory=list)
    estimated_ready_in: str = ""


class RewrittenBullet(BaseModel):
    original: str
    rewritten: str = ""
    keywords_added: List[str] = Field(default_factory=list)
    recommendation: str = ""