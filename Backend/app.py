from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import yfinance as yf
from scipy.optimize import minimize

app = Flask(__name__)
CORS(app)

def portfolio_optimization(returns):
    # Calculate mean returns and covariance of returns
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    # Define number of assets
    num_assets = len(mean_returns)

    # Define the objective function for minimization (negative Sharpe ratio)
    def objective(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_volatility  # Sharpe ratio to be maximized (negated)

    # Constraints: sum of weights = 1
    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]

    # Minimize negative Sharpe ratio
    result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)
    return result.x

@app.route('/api/portfolio_data', methods=['GET'])
def get_portfolio_data():
    # Get tickers and date range from query parameters
    tickers = request.args.get('tickers').split(',')
    start = request.args.get('start')
    end = request.args.get('end')

    if not tickers or not start or not end:
        return jsonify({"error": "Please provide 'tickers', 'start', and 'end' parameters"}), 400

    # Fetch data for each ticker and concatenate adjusted closing prices into a DataFrame
    data = yf.download(tickers, start=start, end=end)['Adj Close']

    if data.empty:
        return jsonify({"error": "No data found for the provided tickers within the specified date range"}), 404

    # Calculate daily returns
    returns = data.pct_change().dropna()

    # Calculate optimal weights using portfolio optimization
    optimal_weights = portfolio_optimization(returns)

    # Format results into JSON serializable format
    portfolio_results = {
        "tickers": tickers,
        "optimal_weights": dict(zip(tickers, optimal_weights)),
        "historical_returns": returns.to_dict(orient='records')
    }

    return jsonify(portfolio_results), 200

if __name__ == '__main__':
    app.run(debug=True)
