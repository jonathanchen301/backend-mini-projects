from fastapi import APIRouter, UploadFile, File

router = APIRouter(
    prefix = "/files",
    tags = ["Files"]
)

@router.post("/upload", summary="Upload a file", description="Upload a file to the server")
async def upload_file(file: UploadFile = File(...)) -> dict[str, str]:
    contents = await file.read()
    return {"filename": file.filename, "preview":contents[:100].decode("utf-8")}