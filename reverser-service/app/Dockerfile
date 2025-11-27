# reverser-service/app/Dockerfile
FROM python:3.11-slim
WORKDIR /usr/src/app

COPY app/requirements.txt .

# Copy the proto file
COPY proto/text_pipeline.proto .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install grpcio grpcio-tools

# Generate the gRPC code INSIDE the container
RUN python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    text_pipeline.proto

# Copy the server code
COPY app/grpc_server.py .
COPY app/rest_server.py .


EXPOSE 50053
EXPOSE 8081

# CMD ["python", "grpc_server.py"]
CMD ["python", "rest_server.py"] 