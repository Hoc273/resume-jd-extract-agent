from pydantic import BaseModel, Field
from typing import List
from schema.experience import Experience

class Resume(BaseModel):
    """ALWAYS use this model to structure your response to the user."""
    is_valid_resume: bool = Field(
        description="True if the input text is genuinely a resume/CV, False if it is not (e.g., random text, other types of documents)."
    )

    profile_summary: str = Field(
        description="A brief summary of the applicant's profile."
    )

    hard_skills: List[str] = Field(
        default=[],
        description="A list of the applicant's hard skills."
    )

    soft_skills: List[str] = Field(
        default=[],
        description="A list of the applicant's soft skills."
    )

    education: List[str] = Field(
        default=[],
        description="A list of the applicant's education."
    )

    work_experience: List[Experience] = Field(
        default=[],
        description="A list of the applicant's work experience."
    )

    years_of_experience: int = Field(
        default=0,
        description="The applicant's years of experience."
    )

    projects: List[str] = Field(
        default=[],
        description="A list of the applicant's projects."
    )

    certifications: List[str] = Field(
        default=[],
        description="A list of the applicant's certifications."
    )

    languages: List[str] = Field(
        default=[],
        description="A list of the applicant's languages."
    )

    