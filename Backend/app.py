from flask import Flask
from flask_cors import CORS
from routes.optimize import optimize_bp  # Importing the blueprint

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Register Blueprint(s)
app.register_blueprint(optimize_bp)

if __name__ == '__main__':
    app.run(debug=True)
