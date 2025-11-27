# app/grpc_server.py
import grpc
import time
import os
from concurrent import futures

# Generated gRPC code
import text_pipeline_pb2 as pb2
import text_pipeline_pb2_grpc as pb2_grpc

# Service 2 details (change 'localhost' to the hostname/IP/container name later)

SERVICE_PORT = 50052 # Service 1 gRPC port

class ValidatorServicer(pb2_grpc.ValidatorServicer):
    """Implements the Validator service methods."""
    
    def __init__(self):
        REVERSER_SERVICE_ADDRESS = os.environ.get(
            'REVERSER_SERVICE_ADDRESS', 
            'dns:///reverser-service:50053'
        )
        # Setup the gRPC client for Service 2 (Reverser)
        self.reverser_channel = grpc.insecure_channel(REVERSER_SERVICE_ADDRESS)
        self.reverser_stub = pb2_grpc.ReverserStub(self.reverser_channel)

    def ValidateAndPass(self, request, context):
        print(f"[{time.time()}] 1. Validator received text: '{request.original_text[:20]}...'")
        
        # 1. Validation Logic
        text_to_process = request.original_text
        metadata = dict(request.metadata)
        
        # Check 1: Length check (Example: must be > 5 characters)
        if len(text_to_process) <= 5:
            metadata['validation_status'] = 'FAILED: Text too short'
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Input text must be longer than 5 characters.')
            return pb2.PipelineText() # Return empty response on failure

        # Check 2: Remove special characters (Simple example: keeps only letters, numbers, spaces)
        cleaned_text = ''.join(c for c in text_to_process if c.isalnum() or c.isspace())
        
        metadata['validation_status'] = 'SUCCESS'
        metadata['validation_time'] = str(time.time())
        
        # 2. Prepare request for Service 2
        next_request = pb2.PipelineText(
            original_text=request.original_text,
            processed_text=cleaned_text, # Pass the cleaned text
            metadata=metadata
        )
        
        print(f"[{time.time()}] 1. Validator passed cleaned text to Reverser: '{cleaned_text[:20]}...'")
        
        # 3. Invoke Service 2 (String Reverser)
        try:
            # This is a synchronous call to the next service
            response_from_reverser = self.reverser_stub.ReverseAndPass(next_request)
            print(f"[{time.time()}] 1. Validator received response from Reverser.")
            return response_from_reverser # Return the final result from the pipeline
        except grpc.RpcError as e:
            print(f"[{time.time()}] Error calling Service 2 (Reverser): {e}")
            context.set_code(e.code())
            context.set_details(f"Pipeline error after Validation: {e.details()}")
            return pb2.PipelineText()

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ValidatorServicer_to_server(ValidatorServicer(), server)
    server.add_insecure_port(f'[::]:{SERVICE_PORT}')
    server.start()
    print(f"[{time.time()}] gRPC Validator Service running on port {SERVICE_PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    # NOTE: In the real setup, you would run this in a multi-process environment or
    # ensure Service 2 is available before the client call happens.
    # For now, we will run the gRPC server only.
    serve_grpc()