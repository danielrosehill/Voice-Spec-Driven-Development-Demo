"""LangGraph Workflow Orchestration for Voice-Spec-Driven Development"""

from langgraph.graph import StateGraph, END
from .state import ProjectState, AgentStatus
from .agents import agent1_node, agent2_node, agent3_node


def should_continue_after_agent1(state: ProjectState) -> str:
    """Determine next step after Agent 1"""
    if state["agent_1_status"] == AgentStatus.COMPLETED:
        return "agent_2"
    else:
        return "error_handler"


def should_continue_after_agent2(state: ProjectState) -> str:
    """Determine next step after Agent 2"""
    if state["agent_2_status"] == AgentStatus.COMPLETED:
        return "agent_3"
    else:
        return "error_handler"


def should_continue_after_agent3(state: ProjectState) -> str:
    """Determine next step after Agent 3"""
    if state["agent_3_status"] == AgentStatus.COMPLETED:
        return "end"
    else:
        return "error_handler"


def error_handler_node(state: ProjectState) -> ProjectState:
    """
    Handle errors in the workflow
    """
    print("\n❌ Workflow Error")
    print(f"Current agent: {state['current_agent']}")
    print(f"Errors: {state['errors']}")

    # Mark as not completed
    state["completed"] = False

    return state


def create_workflow() -> StateGraph:
    """
    Create the LangGraph workflow
    """
    # Create graph
    workflow = StateGraph(ProjectState)

    # Add nodes
    workflow.add_node("agent_1", agent1_node)
    workflow.add_node("agent_2", agent2_node)
    workflow.add_node("agent_3", agent3_node)
    workflow.add_node("error_handler", error_handler_node)

    # Set entry point
    workflow.set_entry_point("agent_1")

    # Add conditional edges
    workflow.add_conditional_edges(
        "agent_1",
        should_continue_after_agent1,
        {
            "agent_2": "agent_2",
            "error_handler": "error_handler"
        }
    )

    workflow.add_conditional_edges(
        "agent_2",
        should_continue_after_agent2,
        {
            "agent_3": "agent_3",
            "error_handler": "error_handler"
        }
    )

    workflow.add_conditional_edges(
        "agent_3",
        should_continue_after_agent3,
        {
            "end": END,
            "error_handler": "error_handler"
        }
    )

    # Error handler leads to END
    workflow.add_edge("error_handler", END)

    return workflow


def compile_workflow():
    """Compile the workflow into an executable graph"""
    workflow = create_workflow()
    return workflow.compile()
