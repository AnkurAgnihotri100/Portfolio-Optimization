import numpy as np
from scipy.optimize import minimize

def portfolio_optimization(returns, strategy='max_sharpe', min_weight=0.05, max_weight=0.7):
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(mean_returns)

    def neg_sharpe(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -portfolio_return / portfolio_std

    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    # Choose objective function based on strategy
    if strategy == 'min_variance':
        objective = portfolio_variance
    else:
        objective = neg_sharpe  # Default: maximize Sharpe

    # Constraints: sum of weights = 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # Bounds for weights
    bounds = tuple((min_weight, max_weight) for _ in range(num_assets))

    # Initial guess: equally weighted
    init_guess = num_assets * [1. / num_assets]

    # Optimization
    result = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    if not result.success:
        raise BaseException("Optimization failed:", result.message)

    return result.x
