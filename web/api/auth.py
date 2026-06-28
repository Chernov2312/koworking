__all__ = ()
from fastapi import APIRouter, HTTPException, Request, status

from config import Tags
from core.security import get_password_hash
from db.dao import UserDAO
from db.models import User
from schemas.auth import RegisterUser
from schemas.user import UserPD

auth_router = APIRouter(tags=[Tags.auth])


@auth_router.post('/register')
async def register_user(request: Request, user: RegisterUser) -> UserPD:
    userdb: User = await UserDAO.get_by_username(user.username)
    if not userdb:
        if user.role == 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Роль admin задаётся только при иницализации'
                ' или специальной функцией',
            )
        data = {
            'username': user.username,
            'password': get_password_hash(user.password1),
            'role': user.role,
        }
        new_user = await UserDAO.add(data)
        return new_user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Пользователь с таким ником уже существует',
    )
