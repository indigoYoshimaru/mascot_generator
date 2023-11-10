from functools import lru_cache


def get_logger(name: str = ""):
    from loguru import logger

    logger.add(f"log/{name}.log")
    return logger


def get_host_info():
    import socket

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return dict(
        hostname=hostname,
        ip_address=ip_address,
    )


# @lru_cache()
# def get_settings():
#     from backend.app_models.settings import AppSetting
#     return AppSetting(cfg_dir='search_api/configs/cfg.yaml')
