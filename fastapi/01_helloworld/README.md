# Hello World

### Description

Hello World API

### Set up

Create a conda environment, activate it, and install dependencies:

```python
conda create -n myenv python=3.10
conda activate myenv
pip install -r requirements.txt
```

Start the backend server:

```python
uvicorn app.main:app --reload
```

### Endpoints

- GET /: get the health of the server
- GET /info: get information about the server

### Documentation

- 127.0.0.1:8000/docs
- 127.0.0.1:8000/redoc