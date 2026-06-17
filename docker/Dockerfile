FROM python:3.11-slim

WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir flask

# 复制代码结构
COPY ./backend ./backend
COPY ./frontend ./frontend
COPY ./storage ./storage
COPY ./data ./data

# 初始化数据库（如果未生成）
RUN python ./backend/models.py

EXPOSE 5000

CMD ["python", "./backend/app.py"]