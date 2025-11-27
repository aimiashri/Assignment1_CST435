from flask import Flask, request, jsonify
import requests, time

app = Flask(__name__)
REST_PORT = 8080  # <-- change per service

NEXT_SERVICE_URL = "http://reverser-service:8081/process"  # <-- change per service

@app.route('/process', methods=['POST'])
def process_text():
    start_time = time.time()
    
    if not request.json or 'text' not in request.json:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    
    text = request.json['text']
    
    # Example service-specific logic:
    processed_text = text[::-1]  # Reverse text for Reverser
    
    # Call next service if exists
    if NEXT_SERVICE_URL:
        resp = requests.post(NEXT_SERVICE_URL, json={"text": processed_text})
        if resp.status_code != 200:
            return jsonify({"error": "Next service failed"}), 500
        processed_text = resp.json()['processed_text']  # Get result from next service
    
    end_time = time.time()
    transaction_time = end_time - start_time
    
    return jsonify({
        "processed_text": processed_text,
        "transaction_time_s": transaction_time
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=REST_PORT)
