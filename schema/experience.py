from pydantic import BaseModel, Field
from typing import List
from schema.responsibilities import ResumeResponsibility

class Experience(BaseModel):
    """ Model representing the work experience entry in a resume."""

    title: str = Field(description="Job title of the applicant")
    company: str = Field(description="Company name where the appicant worked")
    employment_period: str = Field(description="The applicant's tenure at the company")
    responsibilities: List[ResumeResponsibility] = Field(
        default=[],
        description="List of responsibilities"
        )