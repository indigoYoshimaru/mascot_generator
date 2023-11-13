from pydantic import BaseModel
from typing import Text, Any
from sqlalchemy.orm import Session
from backend.utils import app_config, get_logger
from backend.app_models import schemas
from backend.app_models.configs import ModelConfig
from diffusers import AutoPipelineForText2Image
from backend.sql_app.database import SessionLocal

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
            prompt=generation_data.prompt, logo_description=logo_description
        )
    except Exception as e:
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else:
        return formatted_prompt

def load_model():
    from backend.utils import app_config
    from backend.app_models.txt2img import Txt2ImageModel
    import torch.multiprocessing as mp
    mp.set_start_method('spawn', force=True)

    model = Txt2ImageModel(model_cfg = app_config.model_config)
    # model.pipeline.unet.share_memory()
    return model

class Txt2ImageModel(BaseModel):
    cfg: ModelConfig
    pipeline: Any

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, model_cfg: ModelConfig):
        try:
            import torch

            pipeline = AutoPipelineForText2Image.from_pretrained(
                model_cfg.model_name,
                torch_dtype=torch.float16,
            )
            pipeline.unet.load_attn_procs(model_cfg.lora_model_path)
            pipeline.to(model_cfg.device)

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")
            raise e
        else:
            super().__init__(cfg=model_cfg, pipeline=pipeline)

    def save(self, db: Session, generation: Any):
        try:
            from datetime import datetime
            from backend.sql_app import crud

            curr_dt = datetime.now()
            end_time = int(round(curr_dt.timestamp()))
            generation.status = 'DONE'
            generation.queue_no = 0
            generation.end_time = end_time
            updated_generation = crud.update_model_run_all(
                db,
                generation = generation,
            )

        except Exception as e:
            logger.error(f"{type(e).__name__}: {e} in model saving")
            raise e
        else:
            logger.info(f"Updated generation info")
            return updated_generation

    def run(self, db: Session):
        from backend.sql_app import crud
        import time
        while True:
            try:
                generation = crud.get_generation_in_queue_for_model(db)
                assert generation, 'No generation found. Skipping model inference'
                logger.info(f"{generation.id=}")
                prompt = crud.get_prompt_by_id(
                    db, prompt_id=generation.prompt_id
                ).prompt
                image_path = crud.get_image_by_id(db, image_id=generation.image_id).path
                logger.info(f"{prompt=}")
                logger.info(f"{image_path=}")
                image = self.pipeline(
                    prompt=prompt,
                    **self.cfg.hyper_params,
                ).images[0]

                image.save(image_path)
                
            except Exception as e:
                
                logger.error(f"{type(e).__name__}: {e} in model inference")
                time.sleep(10)
                continue
            else: 
                updated_generation = self.save(db, generation)
                logger.info(f'{updated_generation.end_time=}')
                time.sleep(3)
                continue


