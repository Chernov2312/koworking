__all__ = ()
from datetime import date, time
from uuid import UUID

from sqlalchemy import (
    INTEGER,
    Date,
    ForeignKey,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class User(Base):
    username: Mapped[str] = mapped_column(
        String(25), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    role: Mapped[str] = mapped_column(String(), default='')

    bookings: Mapped[list['Booking']] = relationship(
        'Booking', back_populates='user'
    )


class Room(Base):
    number: Mapped[int] = mapped_column(INTEGER, unique=True, nullable=False)

    slots: Mapped[list['Slot']] = relationship(
        'Slot',
        back_populates='room',
        cascade='all, delete-orphan',
    )


class Booking(Base):
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    slot_id: Mapped[UUID] = mapped_column(
        ForeignKey('slots.id', ondelete='CASCADE'),
        nullable=False,
    )
    booked_for: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    user: Mapped['User'] = relationship('User', back_populates='bookings')
    slot: Mapped['Slot'] = relationship('Slot', back_populates='bookings')

    __table_args__ = (
        UniqueConstraint('slot_id', 'booked_for', name='uq_slot_per_date'),
    )


class Slot(Base):
    room_number: Mapped[int] = mapped_column(
        ForeignKey('rooms.number', ondelete='CASCADE'),
        nullable=False,
    )
    started_at: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )
    ended_at: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    room: Mapped['Room'] = relationship('Room', back_populates='slots')
    bookings: Mapped[list['Booking']] = relationship(
        'Booking', back_populates='slot'
    )
