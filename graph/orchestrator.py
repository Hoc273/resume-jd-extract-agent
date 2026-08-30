from graph.state import JDResumeState
from agent.ResumeExtractAgent import ResumeExtractAgent
from agent.JDExtractAgent import JDExtractAgent
from langgraph.graph import StateGraph, START, END
from functools import partial

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

def build_graph(llm):
    builder = StateGraph(JDResumeState)
    builder.add_node("resume_extract", partial(resume_node, llm=llm))
    builder.add_node("jd_extract", partial(jd_node, llm=llm))
    builder.add_edge(START, "resume_extract")
    builder.add_edge(START, "jd_extract")
    builder.add_edge("resume_extract", END)
    builder.add_edge("jd_extract", END)
    return builder.compile()