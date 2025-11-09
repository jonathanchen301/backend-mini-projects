import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from app.models.story import StoryIn, StoryOut
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="app/views/templates")

# {story_id: StoryOut}
stories_db = {}

router = APIRouter(
    prefix = "/stories",
    tags = ["Stories"]
)

@router.post("/", 
status_code=201,
response_model=StoryOut,
summary="Create a new story",
description="Create a new story and store it in the database")
def create_story(story: StoryIn) -> StoryOut:
    story_id = str(uuid.uuid4())
    story_out = StoryOut(
        story_id = story_id,
        **story.model_dump()
    )
    stories_db[story_id] = story_out
    return story_out

@router.get("/",
response_model=list[StoryOut],
summary="Get stories from database",
description="Get a paginated list of stories from the database")
def get_stories(skip: int = 0, limit: int = 10) -> list[StoryOut]:
    return list(stories_db.values())[skip:skip+limit]

@router.get("/{story_id}",
response_model=StoryOut,
summary="Get a story from database",
description="Get a story from the database by story_id")
def get_story(story_id: str) -> StoryOut:
    if story_id not in stories_db:
        raise HTTPException(status_code=404, detail="Story not found")
    return stories_db[story_id]

@router.post("/{story_id}/cover",
status_code=201,
summary="Upload a cover image for a story",
description="Upload a cover image for a story and store it in the database")
async def upload_cover(story_id: str, file: UploadFile = File(...)) -> dict[str, str]:
    if story_id not in stories_db:
        raise HTTPException(status_code=404, detail="Story not found")
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Requires .jpg or .png file")
    
    contents = await file.read()
    with open(f"app/static/covers/{story_id}.jpg", "wb") as f:
        f.write(contents)

    story = stories_db[story_id]
    updated_story = story.model_copy(update={"has_cover": True})
    stories_db[story_id] = updated_story
    return {"message": "Cover image uploaded successfully"}

@router.get("/{story_id}/view",
summary="Get a story view page",
description="Get a story view page given a story_id")
def view_story(story_id: str, request: Request) -> HTMLResponse:
    if story_id not in stories_db:
        raise HTTPException(status_code=404, detail="Story not found")
    return templates.TemplateResponse(request, "story_view.html", {"story": stories_db[story_id]})