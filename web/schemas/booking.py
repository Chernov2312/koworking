__all__ = ()
from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SlotResponse(BaseModel):
    id: UUID = Field(..., description='ID слота для бронирования')
    started_at: time = Field(..., description='Время начала слота')
    ended_at: time = Field(..., description='Время окончания слота')

    model_config = ConfigDict(from_attributes=True)


class UserBooking(BaseModel):
    id: UUID
    booked_for: date = Field(..., description='Дата бронирования')
    slot: SlotResponse = Field(..., description='Слот бронирования')


class BookingCreate(BaseModel):
    booked_for: date = Field(..., description='Дата бронирования')
    slot_id: UUID = Field(..., description='Слот бронирования')


class BookingResponse(BaseModel):
    id: UUID = Field(..., description='ID созданной брони')
    user_id: UUID = Field(
        ...,
        description='ID сотрудника, который совершил бронирование',
    )
    slot_id: UUID = Field(..., description='ID забронированного слота')
    booked_for: date = Field(..., description='Дата бронирования')

    model_config = ConfigDict(from_attributes=True)


class BookingDelete(BaseModel):
    id: UUID = Field(..., description='Id брони, которую нужно отменить')


class BookingDeleteResponse(BaseModel):
    deleted: bool = Field(..., description='удалено поле или нет')


class CheckFree(BaseModel):
    date_for: date


class FreeRoomsResponse(BaseModel):
    id: UUID = Field(..., description='ID комнаты')
    number: int = Field(..., description='Номер комнаты')

    slots: list[SlotResponse] = Field(
        ...,
        description='Список доступных слотов в этой комнате',
    )

    model_config = ConfigDict(from_attributes=True)
