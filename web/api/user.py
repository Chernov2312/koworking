__all__ = ()
from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException

from config import Tags
from core.security import get_current_active_user
from db.dao import BookingDAO, UserDAO
from schemas.booking import UserBooking
from schemas.user import (
    GetUser,
    GetUserInfoResponse,
    SetUserRole,
    SetUserRoleResponse,
    UserPD,
)

user_router = APIRouter(tags=[Tags.user])


@user_router.get('/my/bookings')
async def get_my_bookings(
    request: Request,
    user: UserPD = Depends(get_current_active_user),
) -> list[UserBooking]:
    bookings = await BookingDAO.get_bookings_by_user_id(current_id=user.id)
    return bookings


@user_router.post('/user_info')
async def get_user_info(
    request: Request,
    target_user: GetUser,
    admin: UserPD = Depends(get_current_active_user),
) -> GetUserInfoResponse:
    if admin.role == 'admin':
        target_user_info = await UserDAO.get_full_user_info(
            target_id=target_user.id,
        )
        return target_user_info
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='У вас недостаточно прав для этой операции',
    )


@user_router.post('/set_role')
async def set_user_role(
    request: Request,
    target_user: SetUserRole,
    admin: UserPD = Depends(get_current_active_user),
) -> SetUserRoleResponse:
    if admin.role == 'admin':
        target_user_info = await UserDAO.set_role(
            target_id=target_user.id,
            target_role=target_user.role,
        )
        return SetUserRoleResponse(set=target_user_info)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='У вас недостаточно прав для этой операции',
    )


@user_router.get('/users')
async def get_all_users_id(
    request: Request,
    admin: UserPD = Depends(get_current_active_user),
) -> list[GetUser]:
    if admin.role == 'admin':
        users = await UserDAO.get_all()
        return users
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='У вас недостаточно прав для этой операции',
    )
