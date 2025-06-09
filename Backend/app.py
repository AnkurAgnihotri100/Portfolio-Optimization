from flask import Flask
from flask_cors import CORS


# Import the Blueprint from routes
from routes.optimize import optimize_bp
from routes.stock_list import stock_list_bp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running! Use /api/optimize with query parameters."

# Register Blueprints after app object creation
app.register_blueprint(stock_list_bp)
app.register_blueprint(optimize_bp)

if __name__ == '__main__':
    app.run(debug=True)
