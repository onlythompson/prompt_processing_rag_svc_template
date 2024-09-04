from fastapi import Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from .authentication import get_current_active_user

class UserInDB(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    hashed_password: str
    roles: List[str] = []

# This would typically come from a database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "roles": ["user"]
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "roles": ["user", "admin"]
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def has_role(required_roles: List[str]):
    async def role_checker(current_user: UserInDB = Depends(get_current_active_user)):
        for role in required_roles:
            if role in current_user.roles:
                return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return role_checker

# Example usage
# async def get_admin_data(current_user: UserInDB = Depends(has_role(["admin"]))):
#     return {"message": "This is admin data", "user": current_user.username}

# async def get_user_data(current_user: UserInDB = Depends(has_role(["user"]))):
#     return {"message": "This is user data", "user": current_user.username}