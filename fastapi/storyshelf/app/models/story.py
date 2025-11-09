from pydantic import BaseModel, Field, constr

class StoryIn(BaseModel):
    title: constr(min_length=3, max_length=100) = Field(..., description="The title of the story")
    author: constr(min_length=2, max_length=50) = Field(..., description="The author of the story")
    content: constr(min_length=10) = Field(..., description="The content of the story")
    genre: str = Field(..., description="The genre of the story")

    class ConfigDict:
        schema_extra = {
            "example": {
                "title": "Alice in Wonderland",
                "author": "Lewis Carroll",
                "content": "Once upon a time, there was a girl named Alice who went on a magical adventure.",
                "genre": "Fantasy"
            }
        }

class StoryOut(StoryIn):
    story_id: str = Field(..., description="The uuid of the story")
    has_cover: bool = Field(description="Whether the story has a cover image", default=False)

    class ConfigDict:
        schema_extra = {
            "example": {
                "story_id": "123e4567-e89b-12d3-a456-426614174000",
                "has_cover": False,
                "title": "Alice in Wonderland",
                "author": "Lewis Carroll",
                "content": "Once upon a time, there was a girl named Alice who went on a magical adventure.",
                "genre": "Fantasy"
            }
        }