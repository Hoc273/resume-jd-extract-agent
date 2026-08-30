from langchain_core.prompts import ChatPromptTemplate
from LangChain import structured_llm

prompt = ChatPromptTemplate.from_messages([
    ("system", "Bạn là trợ lý AI chuyên nghiệp, có khả năng tóm tắt và phân tích CV."),
    ("user", "Trích xuất thông tin từ cv sau: \n\n{resume_text}")
])

chain = prompt | structured_llm

result =chain.invoke({"resume_text":"Nguyễn Thị Anh, 23 tuổi, tốt nghiệp ngành CNTT loại Giỏi năm 2023, có 1 năm kinh nghiệm làm Frontend Developer tại Công ty TechSolutions. Thành thạo ReactJS, JavaScript, HTML/CSS, và có kiến thức về UI/UX. Tìm kiếm cơ hội phát triển sự nghiệp trong môi trường năng động, muốn học hỏi và đóng góp cho sự phát triển của công ty. " 
})

print(result)