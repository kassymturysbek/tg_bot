from flask import Flask, request
import threading
import time
import os
import requests

app = Flask(__name__)

# Variable to track the state
state = {
    "last_checked": None,
    "periodic_data": []
}

# Function to simulate a periodic task
def periodic_task():
    while True:
        # Update the state or perform some action
        state["last_checked"] = time.strftime('%Y-%m-%d %H:%M:%S')
        if len(state["periodic_data"]) > 50:  # Limit stored logs to 50 entries
            state["periodic_data"] = state["periodic_data"][-50:]
        state["periodic_data"].append(f"Checked at {state['last_checked']}")
        print(f"Periodic task ran at {state['last_checked']}")
        
        # Sleep for 10 seconds
        time.sleep(10)

# Function to ping the server to keep it active
def ping_server():
    render_url = os.environ.get('RENDER_URL', 'http://127.0.0.1:5000')  # Replace with your Render app's URL
    while True:
        try:
            # Sending a GET request to your Render app's public URL
            response = requests.get(f"{render_url}/status", timeout=5)
            print(f"Pinged server at {render_url}/status, status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error pinging server: {e}")
        # Ping every 5 minutes (300 seconds)
        time.sleep(300)

# Define an endpoint to check the state
@app.route('/status', methods=['GET'])
def get_status():
    return {
        "status": "Server is running",
        "last_checked": state["last_checked"],
        "periodic_data": state["periodic_data"][-5:]  # Show the last 5 entries
    }

# Start the periodic task in a separate thread
thread = threading.Thread(target=periodic_task, daemon=True)
thread.start()

# Start the pinging function in a separate thread
ping_thread = threading.Thread(target=ping_server, daemon=True)
ping_thread.start()

# Run the Flask app
if __name__ == '__main__':
    # Use the port provided by Render, default to 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)