from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.jwt import verify_token
from app.models.user import User
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    try:
        payload = verify_token(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    user = UserRepository.get_by_email(
        db,
        str(email),
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


def require_role(role: str):

    def checker(
        user: User = Depends(get_current_user),
    ):

        if user.role.value != role:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return user

    return checker