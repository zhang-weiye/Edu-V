import os
import logging
import requests
import base64
from dotenv import load_dotenv
from pathlib import Path

from src.image_generator.graph.types import State


current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

logger = logging.getLogger(__name__)


def scale_image(image_scale: int = 1) -> (int,int):
    """
    根据输入的image scale 调整 state 里图片的长度和宽度
    """
    if image_scale == 4/3:
        return 1280, 960
    elif image_scale == 16/9:
        return 1280, 720
    elif image_scale == 3/4:
        return 960, 1280
    elif image_scale == 9/16:
        return 720, 1280
    else:
        return 1024, 1024
    
class image_generator_node:
    def __init__(self, api_key : str = None, base_url : str = None, model : str = None):
        self.api_key = api_key if api_key else os.getenv("IMAGE_API_KEY")
        if not self.api_key:
            raise ValueError("Please provide API KEY for generating images.")
        self.base_url = base_url if base_url else os.getenv("IMAGE_BASE_URL")
        if not self.base_url:
            raise ValueError("Please provide url for image generating")
        self.model = model if model else os.getenv("IMAGE_MODEL")
        if not self.model:
            raise ValueError("Please provide model for generating images")
        
    def generate_image(self, state: State = None):
        prompt = state.get("prompt", None)
        if not prompt:
            return {"Error": "Prompt can't be empty"}
        # guidance_scale还不知道是干嘛的
        #state.width, state.height = scale_image(state.guidance_scale)
        
        data = {
            "model": self.model,
            "prompt": state.get("prompt"),
            "image_size": f"{state.get("width", 1024)}x{state.get("height", 1024)}",
            "batch_size": 1,
            "num_inference_steps": state.get("num_inference_steps"),
            "guidance_scale": state.get("guidance_scale")
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        logger.info("image generator node is running")
        response = requests.post(self.base_url, headers = headers, json = data)
        response.raise_for_status()
        result = response.json()
        
        if "images" in result and len(result["images"]) > 0:
            image_info = result["images"][0]
            # 只判断url格式
            if "url" in image_info:
                image_url = image_info["url"]
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                image_base64 = base64.b64encode(image_response.content).decode('utf-8')
                logger.info(f"image generated successfully: {image_url}")
                return {
                    "image_url": image_url,
                    "image_base64": image_base64,
                    "error": None
                }
            else:
                return {"error": "API response is unsupported"}
        else:
            return {"error": f"API unusual expected: {result}"}
        

        

        
def image_save_node(state: State = None) -> State:
    """
    保存图片到本地文件
    
    Args:
        state: 包含图片信息的状态
        
    Returns:
        state字典的更新部分
    """
    if not state.get("image_base64"):
        return {"error": "no image data for saving"}
    
    # 自动生成文件名
    import time
    timestamp = int(time.time())
    file_path = f"generated_image_{timestamp}.png"
    
    # 解码base64并保存
    image_data = base64.b64decode(state["image_base64"])
    with open(file_path, 'wb') as f:
        f.write(image_data)
    
    logger.info(f"image has been saved in : {file_path}")
    return {"file_path": file_path}
        
    
    
    
    