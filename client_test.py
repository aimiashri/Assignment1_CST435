# client_test.py
import grpc
import time
import sys
import os

# --- PATH FIX: BEGIN ---
# This ensures the Python interpreter can find the generated proto files
# by adding the 'validator-service/app' directory to the system path.
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'validator-service', 'app')) 
# --- PATH FIX: END ---

try:
    # Now the import should work because the path is fixed
    import text_pipeline_pb2 as pb2
    import text_pipeline_pb2_grpc as pb2_grpc
except ImportError:
    print("ERROR: Failed to import proto files. Ensure the path fix above is correct and generated files exist.")
    exit(1)


SERVICE_1_ADDRESS = 'localhost:50052'

def run_pipeline_test(text):
    """Sends the gRPC request to Service 1 (Validator) and measures transaction time."""
    
    print(f"--- Client: Sending request to Validator (S1) at {SERVICE_1_ADDRESS} ---")
    
    # Start timer for benchmarking
    start_time = time.time() 

    # Connect to Service 1
    with grpc.insecure_channel(SERVICE_1_ADDRESS) as channel:
        stub = pb2_grpc.ValidatorStub(channel)
        
        # Prepare the initial message
        initial_request = pb2.PipelineText(
            original_text=text,
            processed_text=text,
            metadata={'client_start_time': str(start_time)}
        )
        
        try:
            # Call S1 and receive the final response from S5
            response = stub.ValidateAndPass(initial_request)
            end_time = time.time()
            transaction_time = end_time - start_time
            
            print("\n>>> Client: RECEIVED FINAL RESPONSE <<<")
            print(f"Transaction Time: {transaction_time:.4f} seconds")
            
            # S5 returns a formatted JSON string
            print("\nFINAL STRUCTURED RESULT (from S5):\n")
            print(response.processed_text)
            
        except grpc.RpcError as e:
            print(f"\n>>> Client: RPC ERROR OCCURRED <<<")
            print(f"Status Code: {e.code()}")
            print(f"Details: {e.details()}")
            
# --- Run Test ---
if __name__ == '__main__':
    # Ensure containers are running via 'docker compose up -d'
    
    # Test string that will pass through all 5 services
    test_string = "The quick brown fox jumps over the lazy dog 12345."
    run_pipeline_test(test_string)