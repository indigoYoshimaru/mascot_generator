
from pydantic import BaseModel
from typing import Text
from backend.utils import app_config, get_logger
from backend.app_models import schemas

logger = get_logger(__name__)
model_cfg = app_config.model_config


def get_example_prompt(): 
   import random

   logger.info(model_cfg)
   return random.choice(model_cfg.example_prompts)



def merge_prompt(generation_data: schemas.GenerationRequest): 
    try: 
        logo_description = model_cfg.logo_descriptions.get(generation_data.option, 1)

        formatted_prompt = model_cfg.prompt_format.format(
            prompt = generation_data.prompt, 
            logo_description = logo_description
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else: 
        return formatted_prompt

class Txt2ImageModel(BaseModel): 
    ...