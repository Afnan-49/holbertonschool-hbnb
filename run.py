from app import create_app
from flask_cors import CORS # Added this import

app = create_app()
CORS(app) # Added this line to enable cross-origin requests

if __name__ == "__main__":
    # The host "0.0.0.0" ensures it's accessible on your local network
    app.run(host="0.0.0.0", port=5000, debug=True)
