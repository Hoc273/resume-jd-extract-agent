from groq import Groq
from pydantic import BaseModel
from typing import List
import json


class ResumeSummary(BaseModel):
    full_name: str
    years_of_experience: int
    hard_skills: List[str]
    education_level: str

client = Groq(api_key="")

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    max_tokens=500,
    tools=[{
        "type": "function",
        "function": {
            "name": "extract_resume",
            "description": "Trích xuất thông tin tóm tắt từ CV",
            "parameters": ResumeSummary.model_json_schema(),
        }
    }],
    tool_choice={"type": "function", "function": {"name": "extract_resume"}},
    messages=[
        {"role": "user", 
        "content": "summary this CV: Nguyễn Thị Anh, 23 tuổi, tốt nghiệp ngành CNTT loại Giỏi năm 2023, có 1 năm kinh nghiệm làm Frontend Developer tại Công ty TechSolutions. Thành thạo ReactJS, JavaScript, HTML/CSS, và có kiến thức về UI/UX. Tìm kiếm cơ hội phát triển sự nghiệp trong môi trường năng động, muốn học hỏi và đóng góp cho sự phát triển của công ty." 
    } ]
)

# 1. Lấy kết quả từ tool call
tool_call = response.choices[0].message.tool_calls[0]
# 2. Parse chuỗi JSON thành Dict
resume_data = json.loads(tool_call.function.arguments)
# 3. Tạo Pydantic object
resume_obj = ResumeSummary(**resume_data)
print("Kết quả:", resume_obj)
print("Tên:", resume_obj.full_name)
print("Số năm kinh nghiệm:", resume_obj.years_of_experience)
print("Kỹ năng:", resume_obj.hard_skills)

