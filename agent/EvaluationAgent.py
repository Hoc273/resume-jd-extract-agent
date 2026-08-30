from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schema.resume import Resume
from schema.jd import Jd
from schema.evaluation import EvaluationResult

class EvaluationAgent:
    def  __init__(self,llm):
        self.llm =llm
        self.structured_llm = llm.with_structured_output(EvaluationResult)
        self.prompt = self.evaluation_prompt()
        self.chain = self.prompt | self.structured_llm
    def evaluation_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    Your task is to evaluate how well a candidate's resume matches a given job description and 
                    mark a score from 0 to 100 based on the criteria below.

                    Scoring criteria:
                    - **Hard Skills Match: 30 points**
                    - **Soft Skills Match: 5 points**
                    - **Work Experiences Match: 30 points**
                        - Do NOT award experience points for roles **unrelated** to the job description.
                        - For intern, fresher:
                            - Evaluate based on relavant internships, academic projects, persone projects or porfolio work that aligns with the job.
                        - For experiences candidates:
                            - Evaluate based on **quality, relevance, and impact** of work (e.g., problem-solving, outcomes, tools used).
                    - **Years Of Experiences Match: 15 points**
                    - **Education of Score: 10 points**
                    - **Extras (Certifications, Side Project, Award): 10 points**
                    
                   Instructions:
                    - Extract and compare the candidate's **skills**, **experience**, **education**, and **additional qualifications** to the job description.
                    - Apply the scoring rules strictly, especially for experience and education.
                    - Do not award points for irrelevant experience.

                    You must return a structured JSON response with:
                    1. **total_score**: Total score (0-100)
                    2. **score_breakdown**: Object with individual scores:
                       - hard_skills_score (0-30)
                       - soft_skills_score (0-5)
                       - work_experience_score (0-30)
                       - years_of_experience_score (0-15)
                       - education_score (0-10)
                       - extras_score (0-10)
                    3. **strengths**: Array of {{category, details}} for major strengths
                       - **category** must be in ENGLISH using one of: "Hard Skills", "Soft Skills", "Work Experience", "Years of Experience", "Education", "Extras"
                       - **details** should be in Vietnamese
                    4. **weaknesses**: Array of {{category, details}} for gaps
                       - **category** must be in ENGLISH using one of: "Hard Skills", "Soft Skills", "Work Experience", "Years of Experience", "Education", "Extras"
                       - **details** should be in Vietnamese
                    5. **missing_hard_skills**: Array of {{skill_name, importance, learning_resources[]}} 
                    6. **summary**: 3-4 line summary covering strengths and missing areas (in Vietnamese)
                    7. **recommendation**: "suitable" if score >= 60, else "not_suitable"
                    8. **recommendation_reason**: REQUIRED - Detailed explanation of why suitable/not suitable (in Vietnamese)
                    
                    Example JSON structure:
                    {{
                      "total_score": 67,
                      "score_breakdown": {{
                        "hard_skills_score": 20,
                        "soft_skills_score": 4,
                        "work_experience_score": 25,
                        "years_of_experience_score": 10,
                        "education_score": 5,
                        "extras_score": 3
                      }},
                      "strengths": [
                        {{"category": "Hard Skills", "details": "Ứng viên có kinh nghiệm vững về Python và Django"}},
                        {{"category": "Work Experience", "details": "Có 3 năm kinh nghiệm làm Backend Developer"}}
                      ],
                      "weaknesses": [
                        {{"category": "Hard Skills", "details": "Thiếu kinh nghiệm về AWS và Docker"}}
                      ],
                      "missing_hard_skills": [
                        {{"skill_name": "AWS", "importance": "critical", "learning_resources": []}}
                      ],
                      "summary": "Ứng viên có nền tảng vững về Python...",
                      "recommendation": "suitable",
                      "recommendation_reason": "Ứng viên phù hợp với vị trí này vì..."
                    }}
                    
                    IMPORTANT: 
                    - Ensure total_score equals the sum of all breakdown scores!
                    - For strengths/weaknesses: **category** field MUST be in English, **details** field in Vietnamese
                    - Generate all OTHER text fields (summary, recommendation_reason, skill details, etc.) in Vietnamese language.
                """,
                ),
                (
                    "user",
                    "Please provide matching score between {resume_text} and {jd_text}",
                ),
            ]
        )

    def evaluate(self, resume, jd):
        resume_text = resume.model_dump_json()
        jd_text = jd.model_dump_json()
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                result = self.chain.invoke({"resume_text": resume_text, "jd_text": jd_text})
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    raise   
