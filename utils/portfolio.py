import pandas as pd

def create_portfolio(stocks, allocations):

    portfolio = pd.DataFrame({
        'Stock': stocks,
        'Allocation': allocations
    })

    return portfolio
