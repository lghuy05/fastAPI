from enum import IntEnum
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()

class Priority(IntEnum):
    LOW = 3
    HIGH = 1
    MEDIUM = 2

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description='Name of todo')
    todo_description: str = Field(..., description='description of the todo')
    priority: Priority = Field(default=Priority.LOW, description='Priority of the todo')

class TodoCreate(TodoBase):
    pass
class Todo(TodoBase):
    todo_id: int = Field(..., description='Unique identifier of the todo')
class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of todo')
    todo_description: Optional[str] = Field(None, description='description of the todo')
    priority: Optional[Priority] = Field(None, description='Priority of the todo')

all_todo  = [
    Todo(todo_id = 1, todo_name = 'Sports', todo_description = 'Go to the gym', priority = Priority.MEDIUM),
    Todo(todo_id = 2, todo_name = 'Read', todo_description = 'Read a book', priority = Priority.LOW),
    Todo(todo_id = 3, todo_name = 'Work', todo_description = 'work on some projects', priority = Priority.HIGH),
    Todo(todo_id = 4, todo_name = 'Coding', todo_description = 'grind leetcode', priority = Priority.MEDIUM),
    Todo(todo_id = 5, todo_name = 'Study', todo_description = 'grind GPA', priority = Priority.MEDIUM)
]

@app.get('/todo/{todo_id}', response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todo:
        if todo.todo_id == todo_id:
            return todo

    raise HTTPException(status_code=404, detail= "Todo not found")
@app.get('/todo')
def get_todos(first_n: Optional[int] = None):
    if first_n:
        return all_todo[:first_n]
    else:
        return all_todo

@app.post('/todo', response_model=Todo)
def create_new_todo(todo: TodoCreate):
    new_todo_id = max(t.todo_id for t in all_todo) + 1
    new_todo = Todo(todo_id = new_todo_id, todo_name = todo.todo_name, todo_description = todo.todo_description, priority=todo.priority)
    all_todo.append(new_todo)
    return new_todo

@app.put('/todo/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, update_todo: TodoUpdate):
    for todo in all_todo:
        if todo.todo_id == todo_id:
            if update_todo.todo_name is not None:
                todo.todo_name = update_todo.todo_name
            if update_todo.todo_description is not None:
                todo.todo_description = update_todo.todo_description
            if update_todo.priority is not None:
                todo.priority = update_todo.priority
            return todo
    raise HTTPException(status_code=404, detail= "Todo not found")

@app.delete('/todo/{todo_id', response_model= Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todo):
        if todo.todo_id == todo_id:
            deleted_todo = all_todo.pop(index)
            return delete_todo
    raise HTTPException(status_code=404, detail= "Todo not found")
