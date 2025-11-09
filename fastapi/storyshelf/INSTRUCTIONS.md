# 📚 StoryShelf API - Step-by-Step Instructions

## 🎯 Overview
Build a complete mini-API where users can create stories, upload cover images, and view story pages. This combines CRUD, file handling, HTML templating, and testing!

---

## 📁 Step 1: Project Setup ✅ COMPLETED

Directory structure created!

---

## 📦 Step 2: Install Dependencies ✅ COMPLETED

`requirements.txt` created with all necessary packages.

---

## 🎨 Step 3: Create Pydantic Models (`app/models/story.py`)

### Research:
- `pydantic.constr` - for string validation with min/max length
- How to use `Field` for default values and descriptions

### Create two models:

**StoryIn:**
- `title`: constrained string (3-100 chars)
- `author`: constrained string (2-50 chars)
- `content`: constrained string (min 10 chars)
- `genre`: regular string

Add a `Config` or `model_config` with `json_schema_extra` containing an example story for the docs.

**StoryOut:**
- Inherits from `StoryIn`
- Adds `story_id`: string (UUID format)
- Adds `has_cover`: boolean (default False)

**Hint:** Look up `constr(min_length=..., max_length=...)`

---

## 🗃️ Step 4: Set Up Storage

In `app/routers/stories.py`, create:
- An in-memory dictionary to store stories (key: story_id, value: story object)
- Import `uuid` module for generating unique story IDs

```python
# Example structure
import uuid

stories_db = {}
```

---

## 🛣️ Step 5: Create the Stories Router (`app/routers/stories.py`)

### Research:
- How to use query parameters for pagination (`skip: int = 0, limit: int = 10`)
- How to slice lists for pagination
- How to save files from `UploadFile`
- How to check file MIME types

### Implement these endpoints:

#### **POST /stories**
- Accept `StoryIn` model
- Generate a unique ID using `str(uuid.uuid4())`
- Create a `StoryOut` object with `has_cover=False`
- Store in your dictionary
- Return the created story
- Use `status_code=201`

#### **GET /stories**
- Accept query parameters: `skip: int = 0`, `limit: int = 10`
- Return a paginated list of stories
- Hint: Convert your dictionary values to a list, then slice it

#### **GET /stories/{story_id}**
- Accept `story_id: str` as path parameter
- Return the story or 404 if not found

#### **POST /stories/{story_id}/cover**
- Accept `story_id: str` and `file: UploadFile = File(...)`
- Validate the story exists (404 if not)
- Validate file type (only `.jpg`, `.png` allowed)
  - Check `file.content_type` is `"image/jpeg"` or `"image/png"`
  - Return 400 if invalid
- Save the file to `app/static/covers/{story_id}.jpg` (or .png)
- Update the story's `has_cover` to `True`
- Return success message

**Hints:**
- Use `async with open(filepath, "wb") as f:` and `await file.read()` to save files
- Check file extension: `file.filename.endswith(('.jpg', '.jpeg', '.png'))`
- Research `Path` from `pathlib` for file path manipulation

### Add router metadata:
```python
router = APIRouter(
    prefix="/stories",
    tags=["Stories"]
)
```

---

## 🏥 Step 6: Create System Router (`app/routers/system.py`)

### Simple health check endpoint:

**GET /health**
- No parameters
- Returns `{"status": "ok"}`
- Use `tags=["System"]`

---

## 🎭 Step 7: Set Up HTML Templating

### Research:
- FastAPI's `Jinja2Templates`
- How to use `templates.TemplateResponse()`
- Basic Jinja2 template syntax (`{{ variable }}`)

### In `app/routers/stories.py`:

1. Import `Jinja2Templates` from `fastapi.templating`
2. Create a templates object: `templates = Jinja2Templates(directory="app/views/templates")`

### Create the template (`app/views/templates/story_view.html`):

Create a simple HTML page that displays:
- Story title in an `<h1>`
- Author in an `<h2>`
- Genre in a `<p>`
- Content in a `<div>` or `<p>`
- Cover image if `has_cover` is true (use Jinja2 `{% if %}` syntax)
  - Image src should be `/static/covers/{story_id}.jpg`

**Hint:** Look up Jinja2 template syntax for variables and conditionals

### Add the endpoint:

**GET /stories/{story_id}/view**
- Accept `story_id` and `request: Request` (you need to import `Request` from `fastapi`)
- Get the story or return 404
- Return `templates.TemplateResponse("story_view.html", {"request": request, "story": story})`

---

## 🏠 Step 8: Set Up Main Application (`app/main.py`)

### Create the FastAPI app with metadata:
```python
app = FastAPI(
    title="StoryShelf API",
    description="A FastAPI-powered microfiction sharing service",
    version="1.0.0"
)
```

### Mount static files:
- Research `StaticFiles` from `fastapi.staticfiles`
- Mount your `app/static` directory at `/static`

### Include routers:
- Import both routers
- Use `app.include_router()` for each (no prefix needed since they're in the routers)

---

## 🧪 Step 9: Write Tests (`tests/test_stories.py`)

### Set up:
- Import `TestClient` from `fastapi.testclient`
- Import your `app` from `app.main`
- Create a pytest fixture for the client
- Consider a fixture to clear storage between tests

### Write at least 5 tests:

1. **test_create_story**
   - POST valid story data
   - Assert status 201
   - Assert response matches expected StoryOut format

2. **test_create_story_invalid_payload**
   - POST story missing `title`
   - Assert status 422

3. **test_get_story**
   - Create a story first
   - GET that story by ID
   - Assert status 200 and data matches

4. **test_upload_invalid_file**
   - Create a story
   - Try to upload a `.pdf` file (fake it with `files={"file": ("test.pdf", b"...", "application/pdf")}`)
   - Assert status 400

5. **test_view_story_page**
   - Create a story
   - GET `/stories/{story_id}/view`
   - Assert status 200
   - Assert `"text/html"` in response headers
   - Assert the story title appears in the response text

**Hints:**
- For file uploads in tests: `client.post(url, files={"file": (filename, content, content_type)})`
- To check HTML content: `assert "expected text" in response.text`

---

## 📝 Step 10: Add Pagination Tests (Optional but Recommended)

Test that:
- Creating 15 stories and calling `GET /stories?skip=0&limit=10` returns 10
- Calling `GET /stories?skip=10&limit=10` returns the remaining 5

---

## ✨ Step 11: Polish Documentation

### In your models:
- Add `json_schema_extra` examples to `model_config`

### In your endpoints:
- Add `summary="..."` and `description="..."` parameters
- Add `response_model=...` to all endpoints that return data

### In your routers:
- Make sure tags are set properly
- Consider adding descriptions to the router itself

---

## 📄 Step 12: Create README.md

Document:
- Project description
- Setup instructions (how to install dependencies)
- How to run the server
- Available endpoints
- How to run tests
- How to view the docs

**Make it look professional!** Use headers, code blocks, and emojis if you like.

---

## 🚀 Step 13: Run Everything

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run tests:**
   ```bash
   pytest -v
   ```

3. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Check the docs:**
   - Visit `http://127.0.0.1:8000/docs`
   - Try creating a story through the UI
   - Upload a cover image
   - Visit `/stories/1/view` in your browser

5. **Verify everything works:**
   - All tests pass ✅
   - Docs look polished ✅
   - Can create stories via API ✅
   - Can upload images ✅
   - HTML page displays correctly ✅

---

## 🎯 Success Criteria

Your project is complete when:
- ✅ All 5+ tests pass
- ✅ All endpoints work as specified
- ✅ Cover image upload validates file types
- ✅ HTML story view page renders correctly
- ✅ Pagination works
- ✅ `/docs` looks polished with examples
- ✅ Code is organized in proper structure
- ✅ README is clear and helpful

---

## 💡 Key Concepts to Research

- **Pagination**: `skip` and `limit` query parameters
- **Jinja2**: Template variables, conditionals, loops
- **File validation**: Checking MIME types and extensions
- **File saving**: Async file writing with `open()` and `await`
- **Path manipulation**: Using `pathlib.Path` for file paths
- **Static file serving**: Accessing uploaded files via `/static/`
- **Request object**: Needed for Jinja2 template responses
- **constr**: Pydantic's constrained string type

---

## 🔥 Bonus Challenges (After Core is Done)

1. Add a **DELETE /stories/{story_id}** endpoint (and delete cover image if exists)
2. Add a **PATCH /stories/{story_id}** endpoint for partial updates
3. Add **genre filtering**: `GET /stories?genre=fantasy`
4. Add a **homepage** at `GET /` that lists all stories as HTML links
5. Add **basic CSS** to make the story view page prettier

---

## 📋 Models Reference

### StoryIn
```python
title: constr(min_length=3, max_length=100)
author: constr(min_length=2, max_length=50)
content: constr(min_length=10)
genre: str
```

### StoryOut
```python
# Inherits from StoryIn
story_id: str  # UUID format
has_cover: bool
```

---

## 🗺️ API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/stories` | Create a new story |
| GET | `/stories` | List stories (paginated) |
| GET | `/stories/{story_id}` | Get one story |
| POST | `/stories/{story_id}/cover` | Upload cover image |
| GET | `/stories/{story_id}/view` | View story as HTML |
| GET | `/health` | Health check |

---

Good luck! 🚀📚

