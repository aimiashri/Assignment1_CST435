# transformer-service/app/grpc_server.py
import grpc
import time
import random 
import os
from concurrent import futures

# Generated gRPC code (pastikan anda sudah salin dari validator-service)
import text_pipeline_pb2 as pb2
import text_pipeline_pb2_grpc as pb2_grpc

# Service 4 details
# Gunakan 'localhost' untuk ujian di satu mesin, atau 'analyzer-service' untuk Docker Compose

SERVICE_PORT = 50054 # Port Servis 3

class TransformerServicer(pb2_grpc.TransformerServicer):
    """Implements the Transformer service methods."""
    
    def __init__(self):
        ANALYZER_SERVICE_ADDRESS = os.environ.get (
            'ANALYZER_SERVICE_ADDRESS',
            'dns:///analyzer-service:50055'
        ) 
        # Setup the gRPC client for Service 4 (Analyzer)
        self.analyzer_channel = grpc.insecure_channel(ANALYZER_SERVICE_ADDRESS)
        # Pastikan Servis 4 didefinisikan sebagai 'Analyzer' dalam .proto
        self.analyzer_stub = pb2_grpc.AnalyzerStub(self.analyzer_channel)

    def TransformAndPass(self, request, context):
        print(f"[{time.time()}] 3. Transformer received text: '{request.processed_text[:20]}...'")
        
        input_text = request.processed_text
        metadata = dict(request.metadata)
        
        # 1. Transformation Logic (Rawak)
        transform_type = random.choice(['uppercase', 'lowercase', 'titlecase'])
        
        if transform_type == 'uppercase':
            transformed_text = input_text.upper()
        elif transform_type == 'lowercase':
            transformed_text = input_text.lower()
        else: # titlecase
            transformed_text = input_text.title()
            
        # Update metadata
        metadata['transformation_type'] = transform_type
        metadata['transformation_time'] = str(time.time())
        
        # 2. Prepare request for Service 4
        next_request = pb2.PipelineText(
            original_text=request.original_text,
            processed_text=transformed_text, # Pass the transformed text
            metadata=metadata
        )
        
        print(f"[{time.time()}] 3. Transformer passed {transform_type} text to Analyzer.")
        
        # 3. Invoke Service 4 (Analyzer)
        try:
            response_from_analyzer = self.analyzer_stub.AnalyzeAndPass(next_request)
            print(f"[{time.time()}] 3. Transformer received response from Analyzer.")
            return response_from_analyzer 
            
        except grpc.RpcError as e:
            print(f"[{time.time()}] Error calling Service 4 (Analyzer): {e}")
            context.set_code(e.code())
            context.set_details(f"Pipeline error after Transformation: {e.details()}")
            return pb2.PipelineText()

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_TransformerServicer_to_server(TransformerServicer(), server)
    server.add_insecure_port(f'[::]:{SERVICE_PORT}')
    server.start()
    print(f"[{time.time()}] gRPC Transformer Service running on port {SERVICE_PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve_grpc()