from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from .authentication import (
    Token, User, authenticate_user, create_access_token,
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from .authorization import has_role, get_admin_data, get_user_data
from datetime import timedelta

def setup_security(app: FastAPI):
    @app.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = await authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @app.get("/users/me/", response_model=User)
    async def read_users_me(current_user: User = Depends(get_current_active_user)):
        return current_user

    @app.get("/admin/")
    async def read_admin_data(admin_data: dict = Depends(get_admin_data)):
        return admin_data

    @app.get("/user/")
    async def read_user_data(user_data: dict = Depends(get_user_data)):
        return user_data

# Usage in main.py
# from cross_cutting.security.security import setup_security
# app = FastAPI()
# setup_security(app)