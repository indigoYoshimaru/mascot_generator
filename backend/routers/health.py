from fastapi import APIRouter, Depends
from backend.utils import get_host_info, get_logger

router = APIRouter()
logger = get_logger(name="health")


@router.get("/health")
def health():
    socket_info = get_host_info()
    logger.info(f"{socket_info=}")
    return dict(msg="App running")
