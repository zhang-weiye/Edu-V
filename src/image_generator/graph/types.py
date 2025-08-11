import os
from tkinter import N
from langgraph.graph import MessagesState
from typing import TypedDict, Optional

class State(MessagesState):
    """
    图片生成流程的状态类,继承自MessagesState。
    用于在图片生成节点中传递和存储相关参数与结果。
    """
    prompt: str  # 图片描述提示词，必填
    width: None | int = 1024  # 图片宽度，默认1024
    height: None | int = 1024  # 图片高度，默认1024
    guidance_scale: None | float = 1  # 引导尺度，影响生成图片的多样性，默认1
    image_url: None | str  # 生成图片的URL
    image_base64: None | str  # 图片的base64编码
    num_inference_steps: None | int = 20  # 推理步数，影响图片质量和生成速度，默认20
    error: None | str  # 错误信息，如有异常则记录
    

    

    
    
    

    