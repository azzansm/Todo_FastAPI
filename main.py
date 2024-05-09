from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List

class TodoItem(BaseModel):
    title: str
    description: str
    completed: bool

app = FastAPI()

todo_items = []

# Create a new Todo item
@app.post("/todo/")
async def create_todo_item(item: TodoItem):
    todo_items.append(item)
    return {"message": "Todo item created successfully", "item": item}

# Get all Todo items
@app.get("/todo/", response_model=List[TodoItem])
async def get_all_todo_items():
    if not todo_items:
        raise HTTPException(status_code=404, detail="No todo items found")
    return todo_items

# Get Todo items by title
@app.get("/todo/by-title/", response_model=List[TodoItem])
async def get_todo_by_title(title: str):
    filtered_items = [item for item in todo_items if title.lower() in item.title.lower()]
    if not filtered_items:
        raise HTTPException(status_code=404, detail="No todo items found with this title")
    return filtered_items

# Update a specific Todo item by its index
@app.put("/todo/{item_index}")
async def update_todo_item(item_index: int, item: TodoItem):
    if item_index < 0 or item_index >= len(todo_items):
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_items[item_index] = item
    return {"message": "Todo item updated successfully", "item": item}

# Delete a specific Todo item by its index
@app.delete("/todo/{item_index}")
async def delete_todo_item(item_index: int):
    if item_index < 0 or item_index >= len(todo_items):
        raise HTTPException(status_code=404, detail="Todo item not found")
    deleted_item = todo_items.pop(item_index)
    return {"message": "Todo item deleted successfully", "deleted_item": deleted_item}