import sys
import datetime
import pandas as pd
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

def get_historical_stock_records(stock_code, period_type, period, frequency_type, frequency):
    my_share = share.Share(stock_code + '.T')
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(period_type, period, frequency_type, frequency)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    tz_jst = datetime.timezone(datetime.timedelta(hours=0))
    dts = map(lambda ts: datetime.datetime.fromtimestamp(int(ts/1000), tz_jst), symbol_data['timestamp'])

    return pd.DataFrame({
            'open': symbol_data['open'],
            'high': symbol_data['high'],
            'low': symbol_data['low'],
            'close': symbol_data['close'],
            'volume': symbol_data['volume']
        }, index=dts)

def get_latest_stock_price(stock_code):
    historical_data = get_historical_stock_records(stock_code, share.PERIOD_TYPE_DAY, 1, share.FREQUENCY_TYPE_MINUTE, 1)
    latest_data = historical_data.tail(1)

    latest_price = None

    try:
        latest_price = latest_data.to_dict('records')[0]['close']
    except:
        print("failed to fetch the latest price")
        sys.exit(1)
    
    return latest_price
