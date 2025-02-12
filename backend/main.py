from flask import Flask
from flask_cors import CORS  # Import CORS
from config import Config
from APIs import api_blueprints
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
# Load configuration
app.config.from_object(Config)

# Enable CORS globally
CORS(app)

# Register blueprints
api_blueprints(app)

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])  # Reads from config