from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/upload-form")
def get_upload_form() -> HTMLResponse:
    with open("static/upload.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    contents = await file.read()
    return {"filename": file.filename, "preview":contents[:100].decode("utf-8")}