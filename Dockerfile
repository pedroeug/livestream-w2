# Etapa 1: build do frontend
FROM node:16 AS frontend-builder
WORKDIR /app/frontend

# copia todo o conteúdo do frontend, incluindo package.json
COPY frontend/ .

# instala dependências e gera o build
RUN npm install
RUN npm run build

# Etapa 2: build do backend
FROM python:3.10-slim
WORKDIR /app

# instala ffmpeg para captura de áudio
RUN apt-get update && apt-get install -y ffmpeg

# instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia o código do backend e serviços
COPY backend/ ./backend
COPY services/ ./services

# copia o build estático do frontend
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# expõe a porta da aplicação
EXPOSE 8000

# comando de inicialização
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
