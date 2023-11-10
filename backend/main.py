import os

from fastapi import FastAPI
from backend.utils import get_logger
from backend.routers import get_all_routers
from fastapi.middleware.cors import CORSMiddleware


# from search_api.models.spelling_corrector import SpellingCorrectorModel
# from search_api.app_models.settings import SpellingCorrectorSettings
# from search_api.handlers.log_writer import LogWriter

# logger = get_logger(name = __name__)

# def number_of_workers():
#     import multiprocessing

#     return int(multiprocessing.cpu_count() / 2)


# def load_model():
#     vsc_setting = SpellingCorrectorSettings(
#         cfg_dir="search_api/configs/vsc_model_cfg.yaml"
#     )
#     return SpellingCorrectorModel(vsc_setting)


try:
    # SPELL_CORRECTOR = load_model()
    # logger.info(f"model loaded: {id(SPELL_CORRECTOR)} - {SPELL_CORRECTOR}")
    # LOG_WRITER = LogWriter(cfg_dir="search_api/configs/json_bin.yaml")
    # logger.info(f"Starting app...")
    app = FastAPI(
        title="Mascot Generator",
        description="Mascot Generator by MLEM",
        version="0.0.1",
        docs_url="/docs",
        redoc_url="/redoc",
        root_path=os.getenv("ROOT_PATH", ""),
    )

    origins = [
        "http://localhost:8001",
        "http://0.0.0.0:8001"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in get_all_routers():
        app.include_router(router)
except Exception as e:
    raise RuntimeError(f"Cannot start app due to error {e}")
