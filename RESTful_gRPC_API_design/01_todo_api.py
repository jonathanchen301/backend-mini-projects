from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

memory = {}
id_sys = 0

class ToDo(BaseModel):
    id : int | None = None
    title : str
    done : bool = False

app = FastAPI()

@app.get("/todos")
def get_todos():
    return list(memory.values()) 

@app.post("/todos")
def create_todo(todo: ToDo):
    global id_sys
    todo.id = id_sys
    memory[id_sys] = todo
    id_sys += 1
    return JSONResponse(
        status_code = 201,
        content = todo.model_dump()
    )

@app.get("/todos/{id}")
def get_todo(id: int):
    if id not in memory:
        return JSONResponse(
            status_code = 404,
            content={"error": "Todo not found"}
        )
    return memory[id].model_dump()


@app.delete("/todos/{id}")
def delete_todo(id: int):
    if id not in memory:
        return JSONResponse(
            status_code = 404,
            content={"error": "Todo not found"}
        )
    else:
        del memory[id]
        return JSONResponse(
            status_code = 200,
            content={
                "message": "Todo deleted successfully",
            }
        )