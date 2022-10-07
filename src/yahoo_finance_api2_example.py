import sys
from datetime import datetime
import pandas as pd
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

my_share = share.Share('7203.T')
symbol_data = None

try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                          1,
                                          share.FREQUENCY_TYPE_MINUTE,
                                          1)
except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

symbol_df = pd.DataFrame({
    'open': symbol_data['open'],
    'high': symbol_data['high'],
    'low': symbol_data['low'],
    'close': symbol_data['close'],
    'volume': symbol_data['volume']
    }, index=map(lambda ts: datetime.fromtimestamp(int(ts/1000)), symbol_data['timestamp']))

print(symbol_df.tail(5))
