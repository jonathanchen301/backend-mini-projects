# StoryShelf API

A FastAPI-powered microfiction sharing service.

## Features

- Create and manage short stories
- Upload cover images for stories
- View stories as formatted HTML pages
- Pagination support
- Full input validation

## Setup

```bash
pip install -r requirements.txt
```

## Run Server

```bash
uvicorn app.main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

## API Documentation

Interactive docs: `http://127.0.0.1:8000/docs`

## Run Tests

```bash
pytest -v
```

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/stories` | Create a new story |
| GET | `/stories` | List stories (paginated) |
| GET | `/stories/{story_id}` | Get story by ID |
| POST | `/stories/{story_id}/cover` | Upload cover image |
| GET | `/stories/{story_id}/view` | View story as HTML |
| GET | `/system/health` | Health check |

## Tech Stack

- FastAPI
- Pydantic
- Jinja2
- pytest