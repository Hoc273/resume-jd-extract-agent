import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agent.ResumeExtractAgent import ResumeExtractAgent
from agent.JDExtractAgent import JDExtractAgent
from agent.EvaluationAgent import EvaluationAgent   # tên file/class bạn đặt, tự chỉnh nếu khác

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.environ["GROQ_API_KEY"])

# Bước 1: trích xuất Resume (dùng lại agent Phase 3)
resume_agent = ResumeExtractAgent(llm)
resume = resume_agent.extract(resume_path="./Nguyen-Le-Hoang-Hoc-TopCV.vn-210726.163640.pdf")
print("=== RESUME ===")
print(resume.model_dump_json(indent=2))

# Bước 2: trích xuất JD (dùng lại agent Phase 3)
jd_agent = JDExtractAgent(llm)
jd = jd_agent.extract(jd_path="./jd.docx")
print("=== JD ===")
print(jd.model_dump_json(indent=2))

# Bước 3: chấm điểm — agent vừa viết ở Phase 5
eval_agent = EvaluationAgent(llm)
result = eval_agent.evaluate(resume, jd)
print("=== EVALUATION RESULT ===")
print(result.model_dump_json(indent=2))