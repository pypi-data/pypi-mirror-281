# File: technical_indicators.py

import numpy as np

def calculate_ema(data, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    ema = np.convolve(data, weights)[:len(data)]
    ema[:window] = ema[window]
    return ema

def calculate_sma(data, window):
    sma = np.convolve(data, np.ones(window), 'valid') / window
    return np.concatenate((np.full(window - 1, np.nan), sma))

def calculate_rsi(data, window=14):
    delta = np.diff(data)
    gain = delta * (delta > 0)
    loss = -delta * (delta < 0)
    avg_gain = calculate_sma(gain, window)
    avg_loss = calculate_sma(loss, window)
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return np.concatenate((np.full(window, np.nan), rsi))

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = calculate_ema(data, short_window)
    long_ema = calculate_ema(data, long_window)
    macd_line = short_ema - long_ema
    signal_line = calculate_ema(macd_line, signal_window)
    return macd_line, signal_line
