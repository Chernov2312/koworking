FROM python:3.13-slim

LABEL maintainer="Max"
LABEL description="ToDo приложение"

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y bash

COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/dev.txt

COPY . .

CMD ["python", "web/main.py"]