from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize

# Define the Blueprint
optimize_bp = Blueprint('optimize', __name__)

# ---- Portfolio Optimization Logic ----
def portfolio_optimization(returns):
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(mean_returns)

    def objective(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_volatility  # Maximize Sharpe ratio (negated)

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]

    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)
    return result.x

# ---- API Route ----
@optimize_bp.route('/api/portfolio_data', methods=['GET'])
def get_portfolio_data():
    tickers = request.args.get('tickers')
    start = request.args.get('start')
    end = request.args.get('end')

    if not tickers or not start or not end:
        return jsonify({"error": "Please provide 'tickers', 'start', and 'end' parameters"}), 400

    tickers_list = tickers.split(',')

    # Fetch adjusted close data
    data = yf.download(tickers_list, start=start, end=end)['Adj Close']
    if data.empty:
        return jsonify({"error": "No data found for the provided tickers within the specified date range"}), 404

    # Compute daily returns
    returns = data.pct_change().dropna()
    optimal_weights = portfolio_optimization(returns)

    result = {
        "tickers": tickers_list,
        "optimal_weights": dict(zip(tickers_list, optimal_weights)),
        "historical_returns": returns.to_dict(orient='records')
    }

    return jsonify(result), 200
