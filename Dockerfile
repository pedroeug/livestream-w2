# Etapa 1: build do frontend
FROM node:16 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Etapa 2: build do backend
FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia código
COPY backend/ ./backend
COPY services/ ./services
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# expõe porta
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
