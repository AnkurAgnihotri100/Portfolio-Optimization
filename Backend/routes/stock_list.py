from flask import Blueprint, jsonify

stock_list_bp = Blueprint('stock_list_bp', __name__)

@stock_list_bp.route('/api/stock-list', methods=['GET'])
def stock_list():
    stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "META"]
    return jsonify({"available_stocks": stocks})
