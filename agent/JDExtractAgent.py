from tools.documents_loader import docx_loader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from tools.documents_loader import pdf_loader
from schema.jd import Jd

class JDExtractAgent:
    def __init__(self,llm):
        self.llm = llm
        self.structured_llm = llm.with_structured_output(Jd)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
            """
            Bạn là một trợ lý phân tích mô tả công việc(JD).
            
            Nhiệm vụ của bạn là phân tích mô tả cộng việc nằm giữa ba dấu(```) và trích xuất thông tin có cấu trúc từ đó.

            Đối với mỗi mô tả công việc, bạn phải trích xuất tất cả các trường thông tin bao gồm:

            - job_summary: Bản tóm tắt ngắn gọn về mô tả cộng việc
            - required_hard_skills:  Tất cả những kĩ năng chuyên môn/ kỹ thuật bắt buộc được đề cập
            - optional_hard_skills:  Tất cả những kĩ năng chuyên môn/ kỹ thuật tùy chọn được đề cập
            - require_years_of_experience: Số năm kinh nghiệm yêu cầu tối thiểu
            - required_soft_skills:  Tất cả những kỹ năng mềm bắt buộc được đề cập
            - required_education:  Tất cả những bằng cấp bắt buộc được đề cập
            - optional_education:  Tất cả những bằng cấp tùy chọn được đề cập
            - optional_soft_skills:  Tất cả những kỹ năng mềm tùy chọn được đề cập
            
            Hãy đảm báo trích xuất tất cả thông tin từ mô tả công việc. ĐẶc biệt chú ý đến các yêu cầu về kinh nghiệm làm việc, kỹ năng(cả kỹ năng cứng và kỹ năng mềm) và yêu cầu về học vấn.

            Quan trọng: Tất cả văn bản được trích xuất bằng tiếng việt.
            """
            ),
            ("user","Trích xuất thông tin từ JD sau: ```{jd_text} ```")
        ])
        self.chain = self.prompt | self.structured_llm

    def extract(self, jd_path:str = None, jd_text: str = None) -> Jd:
        if jd_path is not None and jd_text is not None:
            raise ValueError("Chỉ được cung cấp Text hoặc Path , không được cấp cả 2")
        if jd_path is None and jd_text is None:
            raise ValueError("Phải cung cấp ít nhất 1 trong 2 ")
        
        if jd_path is not None:
            if jd_path.endswith(".pdf"):
                jd_text = pdf_loader.invoke(jd_path)
            elif jd_path.endswith(".docx"):
                jd_text = docx_loader.invoke(jd_path)
            else:
                raise ValueError("Invalid file type. Only .pdf and .docx are supported.")
        if len(jd_text.strip()) < 30:
            raise ValueError("JD quá ngắn hoặc không hợp lệ")
        
        result = self.chain.invoke({"jd_text":jd_text})
        return result
            

