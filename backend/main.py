import os

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from backend.routers import get_all_routers
from fastapi.middleware.cors import CORSMiddleware
from backend.sql_app.database import engine
from backend.sql_app import crud, models, database
from backend.app_models import schemas
# logger = get_logger(name = __name__)

subapi = FastAPI()


@subapi.get("/run-model")
def run_model():
    try: 
        from backend.app_models.txt2img import load_model
        model = load_model()
        db = database.SessionLocal()
        # mp.set_start_method('spawn')
        # queue = mp.Queue()
        # pf = mp.Process(target=model.run, args=(queue, db,), daemon=True)
        # pf.start()
        # pf.join()
        # mp.spawn(model.run, args=(db,), nprocs=1)
        model.run(db)
    except Exception as e: 
        print(e)
        raise e 

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
    
    app.mount("/subapi", subapi)
    
    
except Exception as e:
    print(e)
    raise RuntimeError(f"Cannot start app due to error {e}")
