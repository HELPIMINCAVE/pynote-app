FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
COPY src/ .
COPY notes_db.json .
LABEL authors="mcbookair"

ENTRYPOINT ["python", "main/main.py"]