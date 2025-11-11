from fastapi import Request
from fastapi.responses import Response
import uuid
import time
from app.logger import logger

async def middleware(request: Request, call_next) -> Response:
    if request.headers.get("X-Request-ID"):
        request.state.request_id = request.headers.get("X-Request-ID")
    else:
        request.state.request_id = str(uuid.uuid4())

    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    duration = (end_time - start_time) * 1000

    logger.info("Request processed", 
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration,
            "request_id": request.state.request_id,
        }
    )

    response.headers["X-Request-ID"] = request.state.request_id
    return response