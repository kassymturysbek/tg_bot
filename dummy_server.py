from flask import Flask, request
import threading
import time
import os

app = Flask(__name__)

# Variable to track the state (you can modify this as needed)
state = {
    "last_checked": None,
    "periodic_data": []
}

# Function to simulate a periodic task
def periodic_task():
    while True:
        # Update the state or perform some action
        state["last_checked"] = time.strftime('%Y-%m-%d %H:%M:%S')
        state["periodic_data"].append(f"Checked at {state['last_checked']}")
        
        # Print to console for debugging (optional)
        print(f"Periodic task ran at {state['last_checked']}")
        
        # Sleep for 10 seconds
        time.sleep(10)

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

# Run the Flask app
if __name__ == '__main__':
    # Use the port provided by Render, default to 5000 if not set
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
