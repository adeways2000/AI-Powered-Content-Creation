from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from agents.langchain_agents import (
    research_tool,
    outline_tool,
    writer_tool,
    editor_tool,
    seo_tool
)

# Define state type
from typing import TypedDict


class AgentState(TypedDict):
    topic: str
    tone: str
    context: str
    outline: str
    draft: str
    final: str
    keywords: str

# Node: Research
def research_node(state: AgentState) -> AgentState:
    context = research_tool.invoke(state["topic"])
    return {**state, "context": context}
    

# Node: outline
def outline_node(state: AgentState) -> AgentState:
    outline = outline_tool.invoke({
        "topic": state["topic"],
        "context": state["context"]
    })
    return {**state, "outline": outline}


# Node: writer
def writer_node(state: AgentState) -> AgentState:
    draft = writer_tool.invoke({
        "topic": state["topic"],
        "outline": state["outline"]
    })
    return {**state, "draft": draft}


# Node: Editor (with tone)
def editor_node(state: AgentState) -> AgentState:
    # Ensure tone is always provided with fallback
    tone = state.get("tone") or "Professional"  # Handle None/missing cases
    final = editor_tool.invoke({
        "draft": state["draft"],
        "tone": tone  # Now guaranteed to be a string
    })
    return {**state, "final": final}

# Node: SEO
def seo_node(state: AgentState) -> AgentState:
    keywords = seo_tool.invoke(state["final"])
    return {**state, "keywords": keywords}

# Build Graph
builder = StateGraph(AgentState)

builder.add_node("research_node", RunnableLambda(research_node))
builder.add_node("outline_node", RunnableLambda(outline_node))
builder.add_node("writer_node", RunnableLambda(writer_node))
builder.add_node("editor_node", RunnableLambda(editor_node))
builder.add_node("seo_node", RunnableLambda(seo_node))


builder.set_entry_point("research_node")
builder.add_edge("research_node", "outline_node")
builder.add_edge("outline_node", "writer_node")
builder.add_edge("writer_node", "editor_node")
builder.add_edge("editor_node", "seo_node")
builder.set_finish_point("seo_node")

# Export graph
graph = builder.compile()