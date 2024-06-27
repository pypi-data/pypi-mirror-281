# quant_indicators

Python package for financial technical indicators.

## Installation

You can install the package via pip:

```bash
pip install quant_indicators
```

## Usage

from quant_indicators import ema

data = [10, 12, 15, 14, 13, 16, 18]
period = 3

ema_value = ema.calculate_ema(data, period)
print(f"EMA: {ema_value}")

