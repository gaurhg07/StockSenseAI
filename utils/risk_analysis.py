import numpy as np

def calculate_volatility(data):

    returns = data['Close'].pct_change()

    volatility = returns.std() * np.sqrt(252)

    return volatility


def sharpe_ratio(data):

    returns = data['Close'].pct_change().dropna()

    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)

    return sharpe
