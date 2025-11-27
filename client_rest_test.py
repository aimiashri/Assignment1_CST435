import requests
import time

REST_URL = "http://localhost:8080/process"   # S1 REST endpoint

def run_rest_test(text):
    """Sends REST request to S1 and measures total transaction time."""
    
    print(f"--- Client: Sending request to REST service at {REST_URL} ---")
    
    payload = {"text": text}

    start_time = time.time()

    try:
        response = requests.post(REST_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(">>> REST ERROR OCCURRED <<<")
        print("Error:", e)
        return
    
    end_time = time.time()
    transaction_time = end_time - start_time

    data = response.json()

    print("\n>>> Client: RECEIVED FINAL RESPONSE (from Service 5) <<<")
    print("REST Status:", response.status_code)

    # Services return {"processed_text": "...", "transaction_time_s": ...}
    final_output = data.get("processed_text", "(missing)")
    service_time = data.get("transaction_time_s", "(not provided)")

    print(f"\nFINAL RESULT: {final_output}")
    print(f"Time measured by Service 1: {service_time} seconds")
    print(f"Total Client Transaction Time: {transaction_time:.4f} seconds\n")


if __name__ == "__main__":
    test_string = "The quick brown fox jumps over the lazy dog 12345."
    run_rest_test(test_string)
