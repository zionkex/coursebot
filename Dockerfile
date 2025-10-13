FROM python:3.12-slim
WORKDIR /app/bot
COPY ./ ./
RUN pip install uv
RUN uv venv
RUN uv sync 