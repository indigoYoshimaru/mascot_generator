import os

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from backend.utils import get_logger
from backend.routers import get_all_routers
from fastapi.middleware.cors import CORSMiddleware
from backend.sql_app.database import SessionLocal, engine
from backend.sql_app import crud, models, database
from backend.app_models import schemas

# logger = get_logger(name = __name__)

# def load_model():
#     vsc_setting = SpellingCorrectorSettings(
#         cfg_dir="search_api/configs/vsc_model_cfg.yaml"
#     )
#     return SpellingCorrectorModel(vsc_setting)


try:

    print(f"Starting app...")
    models.Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title="Mascot Generator",
        description="Mascot Generator by MLEM",
        version="0.0.1",
        docs_url="/docs",
        redoc_url="/redoc",
        root_path=os.getenv("ROOT_PATH", ""),
    )

    app.mount("/frontend", StaticFiles(directory ="frontend", html=True), name = "frontend" )

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
    print(e)
    raise RuntimeError(f"Cannot start app due to error {e}")
