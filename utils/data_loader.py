import yfinance as yf

def load_stock_data(ticker, period="1y"):
    stock = yf.download(ticker, period=period)
    return stock
