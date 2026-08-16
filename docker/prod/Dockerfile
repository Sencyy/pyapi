FROM python:3.13.15

RUN apt update && apt install sqlite3

RUN mkdir -p /app

COPY requirements.txt /app/requirements.txt
COPY create_db.sh /app/create_db.sh
COPY src /app/src
COPY static /app/static

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN sh create_db.sh

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0"]
