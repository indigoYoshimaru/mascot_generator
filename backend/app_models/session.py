from pydantic import BaseModel
from uuid import UUID, uuid4
from fastapi import HTTPException, Response
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.backends.session_backend import BackendError
from backend.utils import get_logger

logger = get_logger(__name__)

class SessionData(BaseModel):
    visitor_id: str


cookie_params = CookieParameters()

# Uses UUID
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
backend = InMemoryBackend[UUID, SessionData]()


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

async def create_session(visitor_id: str, response: Response):
    try:
        session = uuid4()
        data = SessionData(visitor_id=visitor_id)
        await backend.create(session, data)
        cookie.attach_to_response(response, session)
    except BackendError as e: 
        logger.error(f"{type(e).__name__}: {e}")

        if str(e) == "create can't overwrite an existing session": 
            return 'available session'
        else: 
            raise e

    except Exception as e: 
        logger.error(f"{type(e).__name__}: {e}")
        raise e
    else: 
        return session
    
async def delete_session(session_id, response):
    await backend.delete(session_id)
    cookie.delete_from_response(response)
