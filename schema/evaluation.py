from pydantic import BaseModel,Field, field_validator
from typing import List, Literal, Optional

class ScoreBreakdown(BaseModel):
    """Detailed score breakdown for each evaluation category. """

    hard_skills_score: int = Field(
        ...,
        ge =0,
        le =30,
        description="Score for hard/technical skills match (0-30 points)",
    )

    soft_skills_score: int = Field(
        ...,
        ge =0,
        le=5,
        description= "Score for soft skills match (0-5) point"
    )

    work_expericence_score: int =Field(
        ...,
        ge=0,
        le=30,
        description="Score for work experience match (0-30 points)"
    )

    education_score: int = Field(
        ...,
        ge=0,
        le=10,
        description="Score for education level match (0-10 points)"
    )

    years_of_exp_score: int = Field(
        ...,
        ge=0,
        le=15,
        description="Score for years of experience match (0-15 points)"
    )

    extras_score: int = Field(
        ...,
        ge=0,
        le=10,
        description="Score for extra qualifications (0-10 points)"
    )

    @property
    def total_score(self) -> int:
        """Calculate total score."""
        return (
            self.hard_skills_score
            + self.soft_skills_score
            + self.work_expericence_score
            + self.education_score
            + self.years_of_exp_score
            + self.extras_score
        )
    
    
class MatchStrength(BaseModel):
    """Areas where candicate is strong."""
    
    category: str = Field(...,description = "e.g., 'Hard skills', 'Experience'" )
    details: str= Field(...,description="Brief explantion of why this is a strength")

class MatchWeaknesses(BaseModel):
    """Areas where candicate is lacking"""
    category: str = Field(...,description = "e.g., 'Hard skills', 'Experience'")
    details: str= Field(...,description="Brief explanation of why this is a weakness")

class SkillGap(BaseModel):
    """Information about a misssing skill."""
    skill_name:str = Field(
        ...,description="Name of the missing hard skill"
        )
    importance: Literal["critical","important","nice-to-have"] = Field(
        ...,description="Importance of the missing hard skill",
    )

class EvaluationResult(BaseModel):
    """Complete structured evaluation results of candidate resume against job description."""

    total_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Total score (0-100 points)"
    )

    score_breakdown: ScoreBreakdown = Field(
        ..., description = "Detailed breakdown of scores by category"
    )
    
    strengths: List[MatchStrength] = Field(
        default=[],
        description = "Major strengths of the candidate for this role"
    )

    weaknesses: List[MatchWeaknesses] = Field(
        default=[],
        description = "Major gaps or missing areas"
    )

    missing_hard_skills: List[SkillGap] = Field(
        default=[],
        description = "Missing hard/technical skills"
    )

    summary: str = Field(
        ...,
        min_length=50,
        max_length=500,
        description="3-4 line summary covering strengths and gaps",
    )
    
    recommendation: Literal["suitable","not_suitable"] = Field(
        ..., description="Whether the JD is suitable for this resume"
    )

    recommendation_reason: str = Field(
        default="", description="Detailed reason for the recommendation"
    )

@field_validator("total_score")
@classmethod
def validate_total_score(cls, v, info):
    """Validate total score matches sum of breakdown scores."""
    if "score_breakdown" in info.data:
        calculated = info.data["score_breakdown"].total_score
        if v != calculated:
            raise ValueError(
                f"total_score ({v}) phải bằng tổng score_breakdown ({calculated})"
            )
    return v