from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for the User
class User(BaseModel):
    id: int
    name: str
    email: str

# In-memory "database"
users_db = []

# Create a new user
@app.post("/users/", response_model=User)
def create_user(user: User):
    for u in users_db:
        if u.id == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    users_db.append(user)
    return user

# Get all users
@app.get("/users/", response_model=List[User])
def get_users():
    return users_db

# Get a specific user by ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Update an existing user
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Delete a user
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[idx]
            return user
    raise HTTPException(status_code=404, detail="User not found")
