import sys
import os
from dotenv import load_dotenv


load_dotenv()

from graph.orchestrator import build_graph
from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.environ["GROQ_API_KEY"])
graph = build_graph(llm)

result = graph.invoke({
    "resume_path": "./Nguyen-Le-Hoang-Hoc-TopCV.vn-210726.163640.pdf",
    "jd_path": "./jd.dox",
    "errors": []   # câu hỏi: vì sao cần khởi tạo errors=[] ngay từ đầu, không để thiếu key này?
})

print("=== RESUME ===")
print(result.get("resume").model_dump_json(indent=2))
print("\n=== JD ===")
print(result.get("jd").model_dump_json(indent=2))
print("\n=== ERRORS ===")
print(result.get("errors"))