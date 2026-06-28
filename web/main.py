__all__ = ()
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import auth_router, booking_router, core_router, user_router
from config import seed_initial_data
from db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await seed_initial_data()
    yield

    print('Остановка приложения и закрытие ресурсов...')


app = FastAPI(lifespan=lifespan, title='ToDoList', version='1.0.0')

app.include_router(prefix='', router=core_router)
app.include_router(prefix='/auth', router=auth_router)
app.include_router(prefix='/booking', router=booking_router)
app.include_router(prefix='/user', router=user_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
