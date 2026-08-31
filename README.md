# Resume & JD Matching Agent (AI-Powered)

Hệ thống Agent AI tự động trích xuất, phân tích và chấm điểm mức độ phù hợp giữa **CV (Resume)** và **Mô tả công việc (JD)** sử dụng **LangGraph**, **LangChain**, mô hình ngôn ngữ lớn từ **Groq** và cung cấp REST API qua **FastAPI**.

---

## 📌 Tính năng nổi bật

- **Trích xuất CV đa định dạng**: Hỗ trợ đọc và trích xuất thông tin có cấu trúc từ file `.pdf`, `.docx`.
- **Trích xuất & Xử lý JD**: Hỗ trợ phân tích từ file `.docx`, `.pdf` hoặc chuỗi văn bản (`jd_text`).
- **Xác thực dữ liệu (Input Validation)**: Tự động kiểm tra tính hợp lệ của file CV và JD trước khi xử lý.
- **Workflow tự động hóa với LangGraph**: Quản lý luồng xử lý Multi-Agent (Resume Agent, JD Agent, Evaluation Agent) mạch lạc và có khả năng xử lý lỗi.
- **Đánh giá & Chấm điểm chi tiết**: Phân tích kỹ năng cứng, kỹ năng mềm, kinh nghiệm và đưa ra điểm số kèm nhận xét.
- **Lưu trữ kết quả với SQLite**: Tự động lưu trữ lịch sử chấm điểm vào cơ sở dữ liệu `results.db`.
- **RESTful API với FastAPI**: Hỗ trợ tải file và tra cứu kết quả dễ dàng.

---

## 📂 Cấu trúc dự án

```text
resume/
├── agent/                  # Các AI Agents chuyên biệt
│   ├── ResumeExtractAgent.py  # Agent trích xuất thông tin CV
│   ├── JDExtractAgent.py      # Agent trích xuất thông tin JD
│   └── EvaluationAgent.py     # Agent chấm điểm & đánh giá độ phù hợp
├── database/               # Quản lý Database
│   └── evaluation_db.py       # Kết nối & thao tác với SQLite
├── graph/                  # Luồng LangGraph Orchestrator
│   ├── orchestrator.py        # Xây dựng đồ thị thực thi
│   └── state.py               # State định nghĩa cho luồng xử lý
├── schema/                 # Cấu trúc dữ liệu Pydantic
│   ├── resume.py              # Schema Resume
│   ├── jd.py                  # Schema JD
│   ├── experience.py          # Schema kinh nghiệm làm việc
│   └── evaluation.py          # Schema kết quả đánh giá
├── tools/                  # Công cụ hỗ trợ tải & đọc tài liệu
│   └── documents_loader.py    # Docx & PDF Loader
├── tests/                  # Thư mục chứa các kịch bản test
├── main.py                 # File chạy thử nghiệm dạng Script CLI
├── main_api.py             # File khởi chạy FastAPI Server
├── requirements.txt        # Danh sách thư viện phụ thuộc
└── .env                    # Biến môi trường (chứa GROQ_API_KEY)
```

---

## 🚀 Hướng dẫn cài đặt và chạy

### 1. Yêu cầu hệ thống
- Python >= 3.10
- Khóa API của Groq ([Lấy tại Groq Console](https://console.groq.com/))

### 2. Cài đặt môi trường ảo & dependencies

Mở terminal tại thư mục gốc của dự án:

```bash
# 1. Tạo môi trường ảo (nếu chưa có)
python -m venv .venv

# 2. Kích hoạt môi trường ảo
# Trên Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Trên Windows (CMD):
.venv\Scripts\activate.bat
# Trên Linux/macOS:
source .venv/bin/activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc và cấu hình API key:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 🖥️ Hướng dẫn khởi chạy

### Cách 1: Chạy API Server (Khuyên dùng)

Khởi động server FastAPI bằng `uvicorn`:

```bash
uvicorn main_api:app --reload
```

- Server sẽ chạy tại: `http://127.0.0.1:8000`
- Xem tài liệu tương tác Swagger UI: `http://127.0.0.1:8000/docs`
- Xem tài liệu ReDoc: `http://127.0.0.1:8000/redoc`

#### Các API chính:
1. **`POST /api/score`**: Chấm điểm CV và JD.
   - `resume_file` (File, bắt buộc): File CV (.pdf hoặc .docx).
   - `jd_file` (File, tùy chọn): File JD (.docx hoặc .pdf).
   - `jd_text` (Form text, tùy chọn): Nội dung JD dạng text (cung cấp 1 trong 2: `jd_file` hoặc `jd_text`).
2. **`GET /api/score/{result_id}`**: Lấy kết quả đánh giá theo `result_id`.
3. **`GET /`**: Kiểm tra trạng thái server (Health check).

---

### Cách 2: Chạy thử dạng Script trực tiếp

Chạy script mẫu để kiểm tra nhanh trong terminal:

```bash
python main.py
```

---

## 📝 Quy ước Commit (Conventional Commits)

| Type     | Ý nghĩa                          |
| -------- | -------------------------------- |
| feat     | Thêm tính năng mới               |
| fix      | Sửa lỗi                          |
| refactor | Tối ưu/sửa code không đổi logic  |
| docs     | Cập nhật tài liệu                |
| style    | Format code (khoảng trắng, ...)  |
| test     | Thêm hoặc sửa bài test           |
| chore    | Công việc phụ trợ / bảo trì      |
| perf     | Tối ưu hiệu năng                 |
| build    | Thay đổi build / dependencies    |
| ci       | Cấu hình CI/CD                   |
