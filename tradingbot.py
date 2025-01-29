from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies import Strategy
from lumibot.traders import Trader
from datetime import datetime

API_KEY = 'PKTJ058RCYI38MPVZBZF'
API_SECRET = 'G9sZMMSkbn8VbckfmLuQ2iY3qLOWuxaBUPnU7oOL'
BASE_URL = 'https://paper-api.alpaca.markets/v2'

ALPACA_CREDS = {
    'API_KEY': API_KEY,
    'API_SECRET': API_SECRET,
    'PAPER': True
}

class MLTrader(Strategy):
    def __init__(self, symbol:str='SPY'):
        self.symbol = symbol
        self.sleeptime = '24H'
        self.last_trade = None

    def on_trading_iteration(self):
        if self.last_trade is None:
            order = self.create_order(self.symbol, 10, 'buy', type='market')
            self.submit_order(order)
            self.last_trade = 'buy'

start_date = datetime(2023, 12, 15)
end_date = datetime(2023, 12, 31)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat' broker=broker, parameters={'symbol':'SPY'})
strategy.backtest(YahooDataBacktesting, start=start_date, end=end_date, parameters={'symbol':'SPY'})