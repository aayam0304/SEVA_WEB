from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import os

# --- Basic Setup ---
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- Database Configuration ---
# Get the absolute path of the directory where the script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'visitors.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- Database Model ---
class Counter(db.Model):
    """A simple model to store a single counter value."""
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)


# --- API Route ---
@app.route('/api/visit', methods=['GET'])
def visit_counter():
    """
    This function is called when the website is loaded.
    It increments the visitor count and returns the new total.
    """
    # Try to get the first (and only) counter record from the database
    visitor_count = Counter.query.first()
    
    # If no record exists, create one with a random starting number
    if visitor_count is None:
        # Start count high to look more impressive
        start_count = random.randint(1000, 5000)
        visitor_count = Counter(count=start_count)
        db.session.add(visitor_count)
    else:
        # If a record exists, simply increment its count
        visitor_count.count += 1
        
    # Save the changes to the database
    db.session.commit()
    
    # Return the current count as a JSON object
    return jsonify({'count': visitor_count.count})


# --- Main Execution ---
if __name__ == '__main__':
    # Create the database and table if they don't exist
    with app.app_context():
        db.create_all()
    # Run the Flask app on port 5000
    app.run(debug=True, port=5000)