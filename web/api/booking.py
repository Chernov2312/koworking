__all__ = ()
from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from config import Tags
from core.security import get_current_active_user
from db.dao import BookingDAO, RoomDAO
from db.models import Booking
from schemas.booking import (
    BookingCreate,
    BookingDelete,
    BookingDeleteResponse,
    BookingResponse,
    CheckFree,
    FreeRoomsResponse,
)
from schemas.user import UserPD

booking_router = APIRouter(tags=[Tags.booking])


@booking_router.post('/free')
async def get_free_rooms(
    request: Request,
    date_to_check: CheckFree,
    _: UserPD = Depends(get_current_active_user),
) -> list[FreeRoomsResponse]:
    rooms = await RoomDAO.get_all_free_room(date_to_check.date_for)
    return rooms


@booking_router.post('/create_booking')
async def create_booking(
    request: Request,
    booking_data: BookingCreate,
    user: UserPD = Depends(get_current_active_user),
) -> BookingResponse:
    try:
        new_booking = await BookingDAO.add(
            {
                'user_id': user.id,
                'slot_id': booking_data.slot_id,
                'booked_for': booking_data.booked_for,
            },
        )
        return new_booking

    except IntegrityError as e:
        orig_msg = str(e.orig)
        if (
            'foreign key constraint' in orig_msg
            or 'ForeignKeyViolationError' in orig_msg
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Указанный слот с ID {booking_data.slot_id}'
                ' не существует в системе',
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Этот временной слот уже забронирован на указанную дату',
        )


@booking_router.post('/delete_booking')
async def delete_booking(
    request: Request,
    booking_delete: BookingDelete,
    user: UserPD = Depends(get_current_active_user),
) -> BookingDeleteResponse:
    booking: Booking = await BookingDAO.get_by_id(id=booking_delete.id)
    if booking.user_id != user.id and user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет прав чтобы удалять данную бронь',
        )
    delete_booking = await BookingDAO.delete_booking(booking_delete.id)
    if delete_booking == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Данное бронирование не найдено',
        )
    return delete_booking
