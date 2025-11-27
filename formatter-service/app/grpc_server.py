# formatter-service/app/grpc_server.py
import grpc
import time
import json
from concurrent import futures

import text_pipeline_pb2 as pb2
import text_pipeline_pb2_grpc as pb2_grpc

SERVICE_PORT = 50056 # Port Servis 5

class FormatterServicer(pb2_grpc.FormatterServicer):
    """Implements the Formatter service methods."""
    
    def FormatOutput(self, request, context):
        print(f"[{time.time()}] 5. Formatter received final data from Analyzer.")
        
        # 1. Formatting Logic (Core Function)
        
        metadata = dict(request.metadata)

        # Menyusun data dari metadata dan teks akhir ke dalam format JSON
        final_result = {
            "PIPELINE_STATUS": "SUCCESS",
            "original_input": request.original_text,
            "final_processed_text": request.processed_text,
            "analysis_results": {
                "word_count": metadata.get('analysis_word_count', 'N/A'),
                "vowels": metadata.get('analysis_vowels', 'N/A'),
                "consonants": metadata.get('analysis_consonants', 'N/A'),
            },
            "processing_metadata": {
                "S1_validation_status": metadata.get('validation_status', 'N/A'),
                "S2_transformation_type": metadata.get('transformation_type', 'N/A'),
                "S3_reversal_time": metadata.get('reversal_time', 'N/A'),
                "total_steps_executed": 5
            }
        }
        
        # Tukar hasil akhir kepada string JSON untuk dihantar kembali
        json_output = json.dumps(final_result, indent=2)

        print(f"[{time.time()}] 5. Formatter completed final response.")
        
        # 2. Return the FINAL response
        # Servis ini mengembalikan PipelineText yang mengandungi JSON output
        return pb2.PipelineText(
            processed_text=json_output, 
            metadata=request.metadata # Kembalikan metadata penuh juga
        )

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_FormatterServicer_to_server(FormatterServicer(), server)
    server.add_insecure_port(f'[::]:{SERVICE_PORT}')
    server.start()
    print(f"[{time.time()}] gRPC Formatter Service running on port {SERVICE_PORT}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve_grpc()