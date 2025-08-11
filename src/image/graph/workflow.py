import argparse
import logging
from .types import State
from .builder import create_image_generation_graph

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Image generation Function")
parser.add_argument('--prompt', type=str, help='image description prompt, optional')
args = parser.parse_args()


app = create_image_generation_graph()


initial_state = State(
    prompt=args.prompt if args.prompt else "a boy walking along with a golden retriver by the sandbeach",
    width=1024,
    height=1024,
    num_inference_steps=25,
    guidance_scale=7.5
)

logger.info("Start generating image")
final_state = app.invoke(initial_state)

if final_state.get("error"):
    logger.error(f"Error: {final_state['error']}")
else:
    logger.info("Image generated successfully!")
    logger.info(f"Image URL: {final_state.get('image_url')}")
    logger.info(f"Image saved to: {final_state.get('file_path')}")