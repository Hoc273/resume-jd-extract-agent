from tools.documents_loader import docx_loader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema.resume import Resume
from tools.documents_loader import pdf_loader
import os 
import sys
import json

class ResumeExtractAgent:
    def __init__(self,llm):
        self.llm =llm
        self.structured_llm = llm.with_structured_output(Resume)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
                """Bạn là trợ lý sơ yếu lý lịch chuyên nghiệp.
                nhiệm vụ của bạn là phân tích CV được đặt trong backstrick 3 dấu (```) của ứng viên và trích xuất CV từ đó.
                Nếu văn bản đó không phải CV, đặt is_valid_resume = False và để các field khác rỗng.
                Bỏ qua các thông tin như địa chỉ, email, số điện thoại, ....
                """,
            ),
            ("user","Trích xuất thông tin từ cv sau: ```{resume_text} ```")
        ])
        self.chain = self.prompt | self.structured_llm
        
    def extract(self,resume_path:str)->Resume:
        if resume_path.endswith(".pdf"):
            resume_text = pdf_loader.invoke(resume_path)
        elif resume_path.endswith(".docx"):
            resume_text = docx_loader.invoke(resume_path)
        else:
            raise ValueError("Invalid file type. Only .pdf and .docx are supported.")
        if len(resume_text) < 50:
            raise ValueError("Empty or invalid resume file.")
        result = self.chain.invoke({"resume_text":resume_text})
        return result


