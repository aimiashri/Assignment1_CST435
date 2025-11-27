# reverser-service/app/grpc_server.py
import grpc
import time
import os
from concurrent import futures

# Generated gRPC code
import text_pipeline_pb2 as pb2
import text_pipeline_pb2_grpc as pb2_grpc

# Service 3 details (Transformer)
# MESTI menggunakan nama servis Docker Compose yang betul

SERVICE_PORT = 50053 # Port Servis 2

class ReverserServicer(pb2_grpc.ReverserServicer):
    """Implements the Reverser service methods."""
    
    def __init__(self):
        TRANSFORMER_SERVICE_ADDRESS = os.environ.get(
            'TRANSFORMER_SERVICE_ADDRESS',
            'dns:///transformer-service:50054'
        ) 
        # Setup the gRPC client for Service 3 (Transformer)
        self.transformer_channel = grpc.insecure_channel(TRANSFORMER_SERVICE_ADDRESS)
        self.transformer_stub = pb2_grpc.TransformerStub(self.transformer_channel) 

    def ReverseAndPass(self, request, context):
        print(f"[{time.time()}] 2. Reverser received text: '{request.processed_text[:20]}...'")
        
        input_text = request.processed_text
        
        # 1. String Reversal Logic (Core Function)
        reversed_text = input_text[::-1]
        
        # Update metadata
        metadata = dict(request.metadata)
        metadata['reversal_time'] = str(time.time())
        
        # 2. Prepare request for Service 3
        next_request = pb2.PipelineText(
            original_text=request.original_text,
            processed_text=reversed_text, # Pass the reversed text
            metadata=metadata
        )
        
        print(f"[{time.time()}] 2. Reverser passed reversed text to Transformer.")
        
        # 3. Invoke Service 3 (Transformer)
        try:
            # Synchronous call to the next service
            response_from_transformer = self.transformer_stub.TransformAndPass(next_request)
            print(f"[{time.time()}] 2. Reverser received response from Transformer.")
            return response_from_transformer # Return the result from the rest of the pipeline
            
        except grpc.RpcError as e:
            print(f"[{time.time()}] Error calling Service 3 (Transformer): {e}")
            context.set_code(e.code())
            context.set_details(f"Pipeline error after Reversal: {e.details()}")
            return pb2.PipelineText()

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ReverserServicer_to_server(ReverserServicer(), server)
    server.add_insecure_port(f'[::]:{SERVICE_PORT}')
    server.start()
    print(f"[{time.time()}] gRPC Reverser Service running on port {SERVICE_PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve_grpc()