__all__ = ()
from datetime import time

from sqlalchemy.exc import IntegrityError

from config.settings import settings
from core.security import get_password_hash
from db.dao import RoomDAO, SlotDAO, UserDAO

ROOMS_DATA = [
    {
        'number': 101,
        'slots': [
            {'started_at': time(9, 0), 'ended_at': time(11, 0)},
            {'started_at': time(11, 30), 'ended_at': time(13, 30)},
            {'started_at': time(14, 0), 'ended_at': time(16, 0)},
            {'started_at': time(16, 30), 'ended_at': time(18, 30)},
        ],
    },
    {
        'number': 102,
        'slots': [
            {'started_at': time(10, 0), 'ended_at': time(13, 0)},
            {'started_at': time(14, 0), 'ended_at': time(17, 0)},
        ],
    },
]
ADMINS_DATA = [
    {
        'username': settings.ADMIN_USERNAME,
        'password': get_password_hash(settings.ADMIN_PASSWORD),
        'role': 'admin',
    },
]


async def seed_initial_data():
    for i in ADMINS_DATA:
        try:
            await UserDAO.add(i)
        except IntegrityError:
            continue
    for i in ROOMS_DATA:
        try:
            await RoomDAO.add({'number': i['number']})
            for j in i['slots']:
                try:
                    data = {
                        'room_number': i['number'],
                        'started_at': j['started_at'],
                        'ended_at': j['ended_at'],
                    }
                    await SlotDAO.add(data)
                except IntegrityError:
                    continue
        except IntegrityError:
            continue
