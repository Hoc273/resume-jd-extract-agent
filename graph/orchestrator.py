from graph.state import JDResumeState
from agent.ResumeExtractAgent import ResumeExtractAgent
from agent.JDExtractAgent import JDExtractAgent
from langgraph.graph import StateGraph, START, END
from functools import partial
from agent.EvaluationAgent import EvaluationAgent

def resume_node(state: JDResumeState,llm) -> dict:
    try:
        resume_agent = ResumeExtractAgent(llm)
        resume = resume_agent.extract(resume_path=state["resume_path"])
        return {"resume": resume}
    except Exception as e:
        return {"errors": [f"Error extracting resume: {str(e)}"]}

def jd_node(state: JDResumeState,llm) -> dict:
    try:
        jd_agent = JDExtractAgent(llm)
        jd = jd_agent.extract(jd_path=state["jd_path"])
        return {"jd": jd}
    except Exception as e:
        return {"errors": [f"Error extracting jd: {str(e)}"]}
def evaluation_node(state: JDResumeState, llm) -> dict:
    if state.get("resume") is None or state.get("jd") is None:
        return {"errors": ["Không thể đánh giá vì thiếu resume hoặc jd (bước trích xuất trước đó có thể đã lỗi)"]}
    try:
        eval_agent = EvaluationAgent(llm)
        evaluation = eval_agent.evaluate(state["resume"], state["jd"])
        return {"evaluation": evaluation}
    except Exception as e:
        return {"errors": [f"Error evaluating: {str(e)}"]}

def build_graph(llm):
    builder = StateGraph(JDResumeState)
    builder.add_node("resume_extract", partial(resume_node, llm=llm))
    builder.add_node("jd_extract", partial(jd_node, llm=llm))
    builder.add_node("evaluation", partial(evaluation_node, llm=llm))
    builder.add_edge(START, "resume_extract")
    builder.add_edge(START, "jd_extract")
    builder.add_edge("resume_extract", "evaluation")
    builder.add_edge("jd_extract", "evaluation")
    builder.add_edge("evaluation", END)
    return builder.compile()