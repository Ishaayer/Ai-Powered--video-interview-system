from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

from app.core.jwt import (
    create_access_token,
    create_refresh_token,
)

from app.schemas.user import MessageResponse



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.register(
            db,
            user,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )



@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    try:
        user_data = UserLogin(
            email=form_data.username,
            password=form_data.password,
        )

        return AuthService.login(
            db,
            user_data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )


    
@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    user: User = Depends(get_current_user),
):

    return {
        "access_token": str(
            create_access_token(
                {"sub": str(user.email)}
            )
        ),
        "refresh_token": str(
            create_refresh_token(
                {"sub": str(user.email)}
            )
        ),
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def current_user(
    user: User = Depends(get_current_user),
):
    return user


@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout():

    return MessageResponse(
        message="Logout successful."
    )