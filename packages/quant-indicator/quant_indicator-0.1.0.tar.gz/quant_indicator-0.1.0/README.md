# quant_indicators

Python package for financial technical indicators.

## Installation

You can install the package via pip:

```python
pip install quant_indicators
```

## Usage

```python
import quant_indicator

sticker = 'HPG'
mins = 1

# Create the dataset
df = quant_indicator.create_dataset(sticker, mins)

# Calculate EMA
ema_5 = quant_indicator.EMAIndicator(df['Close'], 5)
df['EMA_5'] = ema_5

print(df)

```