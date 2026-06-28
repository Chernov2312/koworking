__all__ = ()
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from schemas.booking import UserBooking


class UserPD(BaseModel):
    id: UUID
    username: str = Field(..., description='никнейм')
    role: str = Field('employee', description='роль пользователя')


class GetUser(BaseModel):
    id: UUID


class GetUserInfoResponse(UserPD):
    bookings: list[UserBooking] = Field(
        [], description='Бронирования пользователя'
    )


class UserInDB(UserPD):
    password: str
    model_config = ConfigDict(from_attributes=True)
