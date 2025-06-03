# mcp_server.py
from flask import Flask, request, jsonify
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# --- Simulated Train Status Database ---
# In a real-world scenario, this would involve an actual API call to a railway
# data provider. For this example, we're using a static dictionary to simulate
# train status information based on train numbers.
TRAIN_STATUS_DB = {
    "12301": {"name": "Howrah Rajdhani Express", "status": "Running late by 30 minutes, expected arrival at Delhi at 10:30 AM."},
    "12137": {"name": "Punjab Mail", "status": "On time, currently at Itarsi Junction."},
    "12834": {"name": "Howrah Hapa Express", "status": "Cancelled due to operational reasons."},
    "12001": {"name": "Bhopal Shatabdi", "status": "Departed Bhopal on time, currently near Agra."},
    "12627": {"name": "Karnataka Express", "status": "Running 1 hour late, expected arrival at Bangalore at 07:00 PM."},
    "12951": {"name": "Mumbai Rajdhani Express", "status": "Running on time, currently near Vadodara."},
    "11013": {"name": "Coimbatore Express", "status": "Expected to arrive at 11:45 PM, 15 minutes late."},
}

@app.route('/')
def home():
    """
    Root endpoint for the MCP server.
    Provides a simple message to confirm the server is running.
    """
    logging.info("Root endpoint accessed.")
    return "MCP Server is running. Access /tool/get_train_status to use the train status tool."

@app.route('/tool/get_train_status', methods=['POST'])
def get_train_status_tool():
    """
    This endpoint acts as a 'tool' that the AI agent can call.
    It retrieves the simulated status of a train based on its number.

    Expected JSON payload:
    {
        "train_number": "XXXXX"  # A 5-digit string representing the train number
    }

    Returns:
        JSON response with train status or an error message.
    """
    logging.info("Received request for get_train_status tool.")
    data = request.get_json()

    # Validate the incoming request payload
    if not data or 'train_number' not in data:
        logging.warning("Invalid request: 'train_number' missing in payload.")
        return jsonify({"error": "Invalid request. 'train_number' is required."}), 400

    train_number = str(data['train_number']).strip() # Ensure it's a string and remove whitespace

    # Look up the train status in our simulated database
    status_info = TRAIN_STATUS_DB.get(train_number)

    if status_info:
        logging.info(f"Found status for train {train_number}: {status_info['status']}")
        return jsonify({
            "train_number": train_number,
            "name": status_info["name"],
            "status": status_info["status"]
        }), 200
    else:
        logging.info(f"No status found for train number {train_number}.")
        return jsonify({"error": f"Train number '{train_number}' not found or no status available in our database."}), 404

if __name__ == '__main__':
    # Run the Flask application on port 5000.
    # debug=True allows for automatic reloading on code changes and provides a debugger.
    logging.info("Starting MCP Server on port 5000...")
    app.run(port=5000, debug=True)