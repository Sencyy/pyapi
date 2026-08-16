FROM python:3.13.15

RUN apt update && apt install sqlite3

RUN mkdir -p /app/src

COPY requirements.txt /app/requirements.txt
COPY create_db.sh /app/create_db.sh

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN sh create_db.sh
COPY static /app/static

EXPOSE 8000

CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0"]
