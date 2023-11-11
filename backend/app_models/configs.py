from pydantic import BaseSettings
from typing import Dict, Text, List
from optipack.sdk.optipack_utils import file_reader


class ApiConfig(BaseSettings):
    origins: List


class DatabaseConfig(BaseSettings):
    url: Text
    connect_args: Dict
    session_args: Dict


class ModelConfig(BaseSettings):
    device: Text
    model_name: Text
    lora_model_path: Text
    example_prompts: List
    hyper_params: Dict
    logo_descriptions: Dict
    output_image_directory: Text


class AppConfig(BaseSettings):
    db_config: DatabaseConfig
    api_config: ApiConfig
    model_config: ModelConfig

    def __init__(self, cfg_dir: Text):
        try:
            assert cfg_dir, "Invalid path to config file"
            cfg_dict = file_reader.read_yaml(cfg_dir)
            db_config = DatabaseConfig(**cfg_dict["database"])
            api_config = ApiConfig(**cfg_dict["api"])
            model_cfg_dict = file_reader.read_yaml(
                cfg_dict["other_config_paths"]["model_config"]
            )
            model_config = ModelConfig(**model_cfg_dict)
        except:
            raise RuntimeError("Cannot initalize application")
        else:
            super().__init__(
                db_config=db_config,
                api_config=api_config,
                model_config=model_config,
            )
