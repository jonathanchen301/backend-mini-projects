from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import middleware
from fastapi.responses import JSONResponse
from app.logger import logger

app = FastAPI()

@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception",
        extra={
            "method": request.method,
            "path": request.url.path,
            "request_id": request.state.request_id,
            "error_message": str(exc),
        }
    )
    
    return JSONResponse(
        status_code=500,
        content={"error": exc.__class__.__name__, "message": str(exc), "request_id": request.state.request_id}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(middleware)

@app.get("/")
def get_health():
    return {
    "status": "healthy",
    "service": "audit-ready-api-shell"
    }

@app.get("/items")
def get_items():
    return [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"},
    ]

@app.get("/error")
def get_error():
    raise ValueError("This is a test error")