import os

from typing import TypedDict
from langgraph.graph import START, END, StateGraph
from .nodes import image_generator_node, image_save_node
from .types import State

def create_image_generation_graph(
    api_key: str = None, 
    base_url : str = None, 
    model : str = None) -> StateGraph:
    """
    创建图片生成的LangGraph图
    
    Args:
        api_key: 
        base_url:
        model:
        
    Returns:
        配置好的StateGraph实例
    """

    image_generate_node = image_generator_node(api_key, base_url, model)
    

    workflow = StateGraph(State)
    workflow.add_node("generate_image", image_generate_node.generate_image)
    workflow.add_node("save_image", image_save_node)
    workflow.add_edge(START, "generate_image")
    
    def should_save_image(state: State) -> str:
        """决定是否保存图片"""
        if state.get("error"):
            return END
        return "save_image"
    
    workflow.add_conditional_edges(
        "generate_image",
        should_save_image,
        {
            "save_image": "save_image",
            END: END
        }
    )

    workflow.add_edge("save_image", END)
    
    return workflow.compile()