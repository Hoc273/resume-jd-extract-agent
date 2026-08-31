from fastapi import UploadFile, File
from fastapi import FastAPI
from pydantic import BaseModel
import shutil
import uuid
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from graph.orchestrator import build_graph
from graph.state import JDResumeState
from typing import Optional
from fastapi import Form
from database.evaluation_db import init_db, save_result, get_result

app = FastAPI()
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=os.environ["GROQ_API_KEY"])
graph = build_graph(llm)

class GreetRequest(BaseModel):
    name:str

@app.post("/api/score")
async def score(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile= File(None),
    jd_text: Optional[str] = Form(None)
):
    if jd_file is not None and jd_text is not None:
        return{"error": "Pls provide either jd file or jd text"}
    if jd_file is None and jd_text is None:
        return{"error": "Pls provide either jd file or jd text"}
    
    resume_path = await save_upload_temp(resume_file)
    jd_path = None
    if jd_file:
        jd_path = await save_upload_temp(jd_file)
    
    result = graph.invoke({
        "resume_path":resume_path,
        "jd_path":jd_path,
        "jd_text":jd_text,
        "errors":[],
        "evaluation":None
    })

    os.remove(resume_path)
    if jd_path is not None:
        os.remove(jd_path)
    
    result_id = save_result(
        resume_filename=resume_file.filename,
        jd_filename=jd_file.filename if jd_file else "text_input",
        evaluation=result.get("evaluation"),
        errors=result.get("errors")
    )
    
    return {
        "result_id": result_id,
        "evaluation": result.get("evaluation").model_dump() if result.get("evaluation") else None,
        "errors": result.get("errors")
    }


@app.post("/greet")
def greet(request:GreetRequest):
    return {"message":f"Xin chao, {request.name}!"}   

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/upload-test")
async def upload_test(file: UploadFile = File(...)):
    saved_path = await save_upload_temp(file)
    return {"saved_path": saved_path}

@app.get("/api/score/{result_id}")
def get_score_result(result_id: str):
    result = get_result(result_id)
    if result is None:
        return {"error": "Không tìm thấy kết quả với result_id này"}
    return result

async def save_upload_temp(upload_file:UploadFile)->str:
    ext = upload_file.filename.split(".")[-1]
    temp_path = f"temp_uploads/{uuid.uuid4()}.{ext}"
    os.makedirs("temp_uploads", exist_ok=True)
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return temp_path

