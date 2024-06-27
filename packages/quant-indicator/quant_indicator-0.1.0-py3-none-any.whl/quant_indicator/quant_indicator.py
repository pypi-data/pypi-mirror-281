import time
import requests
import pandas as pd
import ta

def fetch_json_from_url(sticker, mins):
    url = f'https://api.vietstock.vn/tvnew/history?symbol={sticker}&resolution={mins}&from=1577811600&to={int(time.time())}'
    referer = 'https://stockchart.vietstock.vn/'

    headers = {'Referer': referer, 'Accept': '*/*', 'User-Agent': 'PostmanRuntime/7.37.3', 'Accept-Encoding': 'gzip, deflate, br'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        res = response.json()
        df = pd.DataFrame(res)
        df['Timestamp'] = pd.to_datetime(df['t'], unit='s', utc=True).dt.tz_convert('Etc/GMT-7').dt.strftime('%Y-%m-%d %H:%M')
        df[['Open', 'Low', 'High', 'Close']] = df[['o', 'l', 'h', 'c']] / 1000
        df['Volume'] = df['v'].astype(int)
        return df[['Timestamp', 'Open', 'Low', 'High', 'Close', 'Volume']]
    
    print(f"Failed to fetch data from URL. Status code: {response.status_code}")
    return None

def create_dataset(sticker, mins):
    df = fetch_json_from_url(sticker, mins)
    if df is not None:
        return df
    else:
        raise ValueError("Failed to create dataset")

def EMAIndicator(close, window, roundNumber=3):
    return ta.trend.EMAIndicator(close, window).ema_indicator().round(roundNumber)