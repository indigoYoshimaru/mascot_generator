from functools import lru_cache

def get_logger(name: str = ''): 
    from loguru import logger
    logger.add(f'log/{name}.log')
    return logger

# @lru_cache()
# def get_settings():
#     from search_api.app_models.settings import AppSetting
#     return AppSetting(cfg_dir='search_api/configs/cfg.yaml')
