from flask import Flask, jsonify
from flask_cors import CORS
import os

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) to allow the website to talk to this backend
CORS(app)

# Define the path for our simple database file
COUNTER_FILE = 'visitor_count.txt'

@app.route('/api/counter', methods=['POST'])
def update_counter():
    """
    This function acts as our API endpoint.
    It reads the current count, increments it, saves it, and returns the new count.
    """
    count = 0
    # Check if the counter file exists
    if os.path.exists(COUNTER_FILE):
        try:
            # Read the current count from the file
            with open(COUNTER_FILE, 'r') as f:
                count = int(f.read())
        except (ValueError, IOError):
            # If the file is empty or corrupted, start from 0
            count = 0
    
    # Increment the count
    new_count = count + 1
    
    try:
        # Write the new count back to the file
        with open(COUNTER_FILE, 'w') as f:
            f.write(str(new_count))
    except IOError as e:
        # If there's an error writing, print it and return an error message
        print(f"Error writing to counter file: {e}")
        return jsonify({'error': 'Could not update count'}), 500

    # Return the new count 
    return jsonify({'count': new_count})

if __name__ == '__main__':
    # Run the Flask app on localhost
    # The debug=True setting allows for automatic reloading when you save changes.
    app.run(debug=True, port=5000)

