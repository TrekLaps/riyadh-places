FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Copy data
COPY ../data/places.json /app/data/places.json

ENV DATABASE_PATH=/app/places.db
ENV DATA_JSON_PATH=/app/data/places.json
ENV HOST=0.0.0.0
ENV PORT=8000
ENV WORKERS=4

EXPOSE 8000

# Import data and start
CMD ["sh", "-c", "python import_data.py /app/data/places.json /app/places.db && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]
