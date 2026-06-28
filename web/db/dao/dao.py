__all__ = ()
from datetime import date
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload

from db.dao.base import BaseDAO
from db.database import connection
from db.models import Booking, Room, Slot, User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    @connection
    async def get_all(cls, *, session: AsyncSession):
        query = select(User)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @connection
    async def get_by_username(cls, username: str, *, session: AsyncSession):
        query = select(User).filter_by(username=username)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def get_full_user_info(
        cls, target_id: UUID, *, session: AsyncSession
    ):
        query = (
            select(User)
            .filter_by(id=target_id)
            .outerjoin(User.bookings)
            .order_by(Booking.booked_for.desc())
            .options(joinedload(User.bookings).joinedload(Booking.slot))
        )
        result = await session.execute(query)
        return result.scalars().first()


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    @connection
    async def get_all_free_room(
        cls, date_to_check: date, *, session: AsyncSession
    ):
        occupied_slots = (
            select(Booking.slot_id)
            .where(Booking.booked_for == date_to_check)
            .scalar_subquery()
        )

        query = (
            select(Room)
            .join(Room.slots)
            .where(Slot.id.not_in(occupied_slots))
            .order_by(Room.number)
            .options(contains_eager(Room.slots))
        )

        result = await session.execute(query)
        return result.scalars().unique().all()


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    @connection
    async def get_bookings_by_user_id(
        cls, current_id: UUID, *, session: AsyncSession
    ):
        query = (
            select(Booking)
            .filter_by(user_id=current_id)
            .order_by(Booking.booked_for.desc())
            .options(joinedload(Booking.slot))
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @connection
    async def delete_booking(cls, booking_id: UUID, *, session: AsyncSession):
        query = delete(Booking).where(Booking.id == booking_id)
        result = await session.execute(query)
        return result.rowcount


class SlotDAO(BaseDAO):
    model = Slot
