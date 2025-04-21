from flask import Flask
from flask_cors import CORS

# Import the Blueprint from routes
from routes.optimize import optimize_bp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running! Use /api/optimize with query parameters."

# Register Blueprint
app.register_blueprint(optimize_bp)

if __name__ == '__main__':
    app.run(debug=True)
