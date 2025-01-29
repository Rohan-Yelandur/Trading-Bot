from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from math import floor

API_KEY = "PKTJ058RCYI38MPVZBZF" 
API_SECRET = "G9sZMMSkbn8VbckfmLuQ2iY3qLOWuxaBUPnU7oOL" 
BASE_URL = "https://paper-api.alpaca.markets/v2"
ALPACA_CREDS = {"API_KEY":API_KEY, "API_SECRET": API_SECRET, "PAPER": True}

start_date = datetime(2023,12,15)
end_date = datetime(2023,12,31) 
symbol:str = 'SPY' # Symbol for stock or ETF to trade
cash_at_risk:float = .5 # Percentage of cash to risk on each trade

class MLTrader(Strategy): 
    def initialize(self, symbol=symbol, cash_at_risk=cash_at_risk): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = floor(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        if cash > last_price:
            if self.last_trade is None:
                order = self.create_order(self.symbol,
                                          quantity,
                                          'buy', 
                                          type='bracket', 
                                          take_profit_price=last_price*1.2,
                                          stop_loss_price=last_price*0.95)
                self.submit_order(order)
                self.last_trade = 'buy'


broker = Alpaca(ALPACA_CREDS) 
strategy = MLTrader(name='mlstrat', broker=broker, parameters={'symbol':'SPY', symbol:cash_at_risk})
strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={'symbol':symbol, 'cash_at_risk':cash_at_risk})
