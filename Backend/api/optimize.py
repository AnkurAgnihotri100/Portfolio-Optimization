@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
    data = request.json
    tickers = data.get('tickers', [])


    optimized_result = your_optimize_function(tickers)

    return jsonify(optimized_result)
