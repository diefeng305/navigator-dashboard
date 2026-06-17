FROM python:3.11-slim

LABEL maintainer="diefeng305"
LABEL description="Navigator Dashboard"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 复制所有文件
COPY . .

# 调试：列出文件
RUN ls -la /app/
RUN ls -la /app/backend/ || echo "backend directory not found"
RUN ls -la /app/frontend/ || echo "frontend directory not found"

RUN mkdir -p /app/data

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/config || exit 1

CMD ["python", "backend/app.py"]