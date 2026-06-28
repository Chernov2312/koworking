from api.auth import auth_router
from api.booking import booking_router
from api.core import core_router
from api.user import user_router

__all__ = ('auth_router', 'core_router', 'booking_router', 'user_router')
