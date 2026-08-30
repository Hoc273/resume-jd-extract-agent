from pydantic import BaseModel, Field
from typing import List

class Jd(BaseModel):
    """ Model representing the job description of an applicant in a resume."""
    
    job_summary: str = Field(description="A brief summary of the job description.")

    required_hard_skills: List[str] = Field(
        default=[],
        description="List of required hard skills."
        )

    optional_hard_skills: List[str] = Field(
        default=[],
        description="List of optional hard skills."
        )

    require_years_of_experience: int = Field(
        default=0,
        description="Required years of experience"
        )

    required_soft_skills: List[str] = Field(
        default=[],
        description="List of required soft skills."
        )
    
    required_education: List[str] = Field(
        default=[],
        description="List of education."
        )
    
    optional_education: List[str] = Field(
        default=[],
        description="List of optional education."
        )
    
    optional_soft_skills: List[str] = Field(
        default=[],
        description="List of optional soft skills."
        )


