from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    from app.routes.routes import zr 
    
    app.register_blueprint(zr)
    app.run(debug=True, host="0.0.0.0", port=9012)
