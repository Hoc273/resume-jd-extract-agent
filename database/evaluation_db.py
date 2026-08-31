import sqlite3
import json
import uuid
from datetime import datetime
from typing import Optional

DB_PATH = "results.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            result_id TEXT PRIMARY KEY,
            resume_filename TEXT,
            jd_filename TEXT,
            evaluation_json TEXT,
            errors_json TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(resume_filename: str, jd_filename: str, evaluation, errors: list) -> str:
    result_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO evaluations (result_id, resume_filename, jd_filename, evaluation_json, errors_json, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (
            result_id,
            resume_filename,
            jd_filename,
            evaluation.model_dump_json() if evaluation else None,
            json.dumps(errors),
            datetime.now().isoformat()
        )
    )
    conn.commit()
    conn.close()
    return result_id

def get_result(result_id: str) -> Optional[dict]:
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM evaluations WHERE result_id = ?", (result_id,)
    ).fetchone()
    conn.close()
    
    if row is None:
        return None
    
    return {
        "result_id": row["result_id"],
        "resume_filename": row["resume_filename"],
        "jd_filename": row["jd_filename"],
        "evaluation": json.loads(row["evaluation_json"]) if row["evaluation_json"] else None,
        "errors": json.loads(row["errors_json"]),
        "created_at": row["created_at"]
    }
init_db()