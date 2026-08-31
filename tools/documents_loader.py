from langchain_community.document_loaders import Docx2txtLoader,PyMuPDFLoader
from langchain_core.tools import tool
import docx2txt
import os

@tool("docx_loader")
def docx_loader(resume_path:str) -> str:
    """A tool to load a DOCX resume and return its text content."""
    try: 
        text = docx2txt.process(resume_path)
        lines= [line.strip() for line in text.split("\n") if line.strip()]
        return "\n".join(lines)
    except Exception as e:
        return "\n".join(
            [page.page_content for page in Docx2txtLoader(resume_path).load()]
        )

@tool("pdf_loader")
def pdf_loader(resume_path:str)->str:
    """A tool to load a PDF resume and return its text content."""
    return "\n".join(
        [page.page_content for page in PyMuPDFLoader(resume_path).load()]
    ) 

if __name__ == "__main__":
    # Đường dẫn tự động trỏ ra thư mục cha (resume/)
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "..", "Nguyen-Le-Hoang-Hoc-TopCV.vn-210726.163640.pdf")
    
    print(pdf_loader.invoke(file_path))