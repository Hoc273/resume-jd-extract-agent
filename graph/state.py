from typing import TypedDict, Optional, Annotated
import operator
from schema.resume import Resume
from schema.jd import Jd
from schema.evaluation import EvaluationResult

class JDResumeState(TypedDict):
    resume_path: Optional[str]
    jd_path: Optional[str]
    jd_text: Optional[str]
    resume: Optional[Resume]
    jd: Optional[Jd]
    errors: Annotated[list, operator.add]
    evaluation: Optional[EvaluationResult]
