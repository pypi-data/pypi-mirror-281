import numpy as np
import pytest
from quant_indicators import calculate_ema, calculate_sma, calculate_rsi, calculate_macd

def test_ema():
    data = np.array([1, 2, 3, 4, 5])
    ema = calculate_ema(data, 3)
    assert np.allclose(ema, np.array([1., 1.5, 2.25, 3.125, 4.0625]))

def test_sma():
    data = np.array([1, 2, 3, 4, 5])
    sma = calculate_sma(data, 3)
    assert np.allclose(sma, np.array([np.nan, np.nan, 2., 3., 4.]))

def test_rsi():
    data = np.array([70, 75, 80, 85, 90])
    rsi = calculate_rsi(data)
    assert np.allclose(rsi, np.array([np.nan, np.nan, np.nan, np.nan, 100.]))

def test_macd():
    data = np.array([12, 14, 16, 18, 20])
    macd_line, signal_line = calculate_macd(data)
    assert np.allclose(macd_line, np.array([0., 0.5, 1., 1.5, 2.]))
    assert np.allclose(signal_line, np.array([0., 0.25, 0.5, 0.75, 1.]))
