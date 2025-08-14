FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
ENV CORS_ALLOW_ORIGINS=http://localhost:8080
EXPOSE 8001
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
