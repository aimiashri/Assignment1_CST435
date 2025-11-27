FROM python:3.11-slim
WORKDIR /usr/src/app

COPY app/requirements.txt .

# Copy proto file and generate gRPC code inside container
#COPY ../../proto/text_pipeline.proto .
COPY proto/text_pipeline.proto .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install grpcio grpcio-tools \
    && python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. text_pipeline.proto

# Copy the server code
COPY app/grpc_server.py .
COPY app/rest_server.py .

# Expose ports for gRPC and REST
EXPOSE 50052
EXPOSE 8080

# CMD ["python", "grpc_server.py"]
CMD ["python", "rest_server.py"] 