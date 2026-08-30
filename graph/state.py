from typing import TypedDict, Optional, Annotated
import operator
from schema.resume import Resume
from schema.jd import Jd

class JDResumeState(TypedDict):
    resume_path: Optional[str]
    jd_path: Optional[str]
    resume: Optional[Resume]
    jd: Optional[Jd]
    errors: Annotated[list, operator.add]

