FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt
COPY notes_db.json /app/notes_db.json

# Copy your source code
COPY src/ /app/src/
LABEL authors="mcbookair"

ENTRYPOINT ["python", "main/main.py"]