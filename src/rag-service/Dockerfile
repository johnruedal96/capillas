FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY app/ .

EXPOSE 50051
CMD ["python", "-m", "grpc_server"]
