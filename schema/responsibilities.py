from pydantic import BaseModel, Field
from typing import List

class ResumeResponsibility(BaseModel):
    """ Model representing the responsibilities of an applicant in a resume."""
    
    task: str = Field(description="The task performed by the applicant")
    tech_stack: str = Field(description="The tech stack used in the task")
    achievements: str = Field(description="Achievements after finish the task")
    