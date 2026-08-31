# test_evaluation.py
from schema.evaluation import EvaluationResult, ScoreBreakdown

try:
    bad_result = EvaluationResult(
        total_score=999,   # cố tình sai để kích hoạt lỗi
        score_breakdown=ScoreBreakdown(
            hard_skills_score=20,
            soft_skills_score=4,
            work_expericence_score=25,
            education_score=5,
            years_of_exp_score=10,
            extras_score=3
        ),
        summary="Đây là một đoạn tóm tắt test dài đủ 50 ký tự để pass validate min_length nhé.",
        recommendation="suitable",
    )
    print("KHÔNG raise lỗi — có vấn đề, kiểm tra lại validator!")
except Exception as e:
    print("Raise lỗi đúng như mong đợi:")
    print(e)