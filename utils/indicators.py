def add_sma(data, window=20):

    data['SMA'] = data['Close'].rolling(window).mean()

    return data


def add_ema(data, window=20):

    data['EMA'] = data['Close'].ewm(span=window).mean()

    return data


def calculate_rsi(data, window=14):

    delta = data['Close'].diff()

    gain = delta.where(delta > 0, 0).rolling(window).mean()

    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()

    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return rsi
