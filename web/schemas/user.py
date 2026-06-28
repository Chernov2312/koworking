__all__ = ()
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.booking import UserBooking


class UserPD(BaseModel):
    id: UUID
    username: str = Field(..., description='никнейм')
    role: str = Field('employee', description='роль пользователя')


class GetUser(BaseModel):
    id: UUID


class SetUserRole(BaseModel):
    id: UUID
    role: str = Field('employee', description='роль пользователя')

    @field_validator('role')
    @classmethod
    def role_validate(cls, value: str) -> str:
        if value is None:
            return None
        if value.lower() not in ['employee', 'admin']:
            raise ValueError('Несуществующая роль. Допустимы: employee, admin')
        return value.lower()


class SetUserRoleResponse(BaseModel):
    set: bool = Field(..., description='Установлена новая роль или нет')


class GetUserInfoResponse(UserPD):
    bookings: list[UserBooking] = Field(
        [],
        description='Бронирования пользователя',
    )


class UserInDB(UserPD):
    password: str
    model_config = ConfigDict(from_attributes=True)
