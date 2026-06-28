__all__ = ()
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class RegisterUser(BaseModel):
    username: str = Field(..., description='никнейм')
    password1: str = Field(..., description='пароль')
    password2: str = Field(..., description='подтверждение пароля')
    role: str = Field('employee', description='роль пользователя')

    @field_validator('password1')
    @classmethod
    def complexity_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Пароль должен содержать не менее 8 символов')
        if not re.search(r'[A-Z]', value):
            raise ValueError(
                'Пароль должен содержать хотя бы одну заглавную букву'
            )
        return value

    @field_validator('role')
    @classmethod
    def role_validate(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if value.lower() not in ['employee', 'admin']:
            raise ValueError('Несуществующая роль. Допустимы: employee, admin')
        return value.lower()

    @model_validator(mode='after')
    def validate_password(self):
        if self.password1 != self.password2:
            raise ValueError('Пароли не совпадают')
        return self


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
