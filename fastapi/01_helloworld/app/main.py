from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title = "Hello World",
    version = "0.1.0",
)

@app.get("/")
def get_root():
    return JSONResponse(
        status_code = 200,
        content = {"status": "OK"}
    )

@app.get("/info")
def get_info():
    return JSONResponse(
        status_code = 200,
        content = {
            "appName": "Hello World",
            "version": "0.1.0",
            "description": "First FastAPI app"
        }
    )