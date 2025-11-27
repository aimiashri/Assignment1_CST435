# analyzer-service/app/grpc_server.py
import grpc
import time
from concurrent import futures
import os
import re

import text_pipeline_pb2 as pb2
import text_pipeline_pb2_grpc as pb2_grpc

# Service 5 details (Formatter - The End)
# MESTI menggunakan nama servis Docker Compose yang betul ('formatter-service')

SERVICE_PORT = 50055 # Port Servis 4

class AnalyzerServicer(pb2_grpc.AnalyzerServicer):
    """Implements the Analyzer service methods."""
    
    def __init__(self):
        FORMATTER_SERVICE_ADDRESS = os.environ.get (
            'FORMATTER_SERVICE_ADDRESS',
            'dns:///formatter-service:50056'
        ) 
        # Setup the gRPC client for Service 5 (Formatter)
        self.formatter_channel = grpc.insecure_channel(FORMATTER_SERVICE_ADDRESS)
        self.formatter_stub = pb2_grpc.FormatterStub(self.formatter_channel)

    def AnalyzeAndPass(self, request, context):
        print(f"[{time.time()}] 4. Analyzer received text: '{request.processed_text[:20]}...'")
        
        input_text = request.processed_text
        metadata = dict(request.metadata)

        # 1. Analysis Logic (Core Function)
        
        # Word Count: Menggunakan regex untuk kira perkataan
        word_count = len(re.findall(r'\b\w+\b', input_text))
        
        char_count = len(input_text)
        
        # Kira Vokal dan Konsonan
        vowels_set = 'aeiou'
        input_lower = input_text.lower()
        
        vowels = sum(1 for char in input_lower if char in vowels_set)
        consonants = char_count - vowels - input_text.count(' ') - input_text.count('\n') 
            
        # Update metadata with analysis results
        metadata['analysis_word_count'] = str(word_count)
        metadata['analysis_char_count'] = str(char_count)
        metadata['analysis_vowels'] = str(vowels)
        metadata['analysis_consonants'] = str(consonants)
        metadata['analysis_time'] = str(time.time())
        
        # 2. Prepare request for Service 5
        next_request = pb2.PipelineText(
            original_text=request.original_text,
            processed_text=input_text, # Pass text as-is to the formatter
            metadata=metadata
        )
        
        print(f"[{time.time()}] 4. Analyzer passed analysis data to Formatter.")
        
        # 3. Invoke Service 5 (Output Formatter)
        try:
            response_from_formatter = self.formatter_stub.FormatOutput(next_request)
            print(f"[{time.time()}] 4. Analyzer received FINAL response from Formatter.")
            return response_from_formatter # Return the final result
            
        except grpc.RpcError as e:
            print(f"[{time.time()}] Error calling Service 5 (Formatter): {e}")
            context.set_code(e.code())
            context.set_details(f"Pipeline error after Analysis: {e.details()}")
            return pb2.PipelineText()

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AnalyzerServicer_to_server(AnalyzerServicer(), server)
    server.add_insecure_port(f'[::]:{SERVICE_PORT}')
    server.start()
    print(f"[{time.time()}] gRPC Analyzer Service running on port {SERVICE_PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve_grpc()