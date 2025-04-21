from flask import Blueprint, request, jsonify
import yfinance as yf
from utils.optimizer import portfolio_optimization

optimize_bp = Blueprint('optimize_bp', __name__)

@optimize_bp.route('/api/portfolio_data', methods=['GET'])
def get_portfolio_data():
    tickers = request.args.get('tickers')
    start = request.args.get('start')
    end = request.args.get('end')

    if not tickers or not start or not end:
        return jsonify({"error": "Please provide 'tickers', 'start', and 'end' parameters"}), 400

    tickers = tickers.split(',')
    raw_data = yf.download(tickers, start=start, end=end)
    print("Downloaded data:\n", raw_data.head())
    data = raw_data['Adj Close']


    if data.empty:
        return jsonify({"error": "No data found for the provided tickers within the specified date range"}), 404

    returns = data.pct_change().dropna()
    optimal_weights = portfolio_optimization(returns)

    portfolio_results = {
        "tickers": tickers,
        "optimal_weights": dict(zip(tickers, optimal_weights)),
        "historical_returns": returns.to_dict(orient='records')
    }

    return jsonify(portfolio_results), 200
