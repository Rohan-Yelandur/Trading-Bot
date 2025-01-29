import os
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from alpaca_trade_api import REST
from timedelta import Timedelta
from datetime import datetime
from math import floor
from sentiment_model import estimate_sentiment

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('BASE_URL')
ALPACA_CREDS = {'API_KEY':API_KEY, 'API_SECRET': API_SECRET, 'PAPER': True}

# ----- Values to customize trading -----
start_date = datetime(2020,1,1) # Start of trading timeframe
end_date = datetime(2023,12,31) # End of trading timeframe
symbol = 'SPY' # Symbol for stock or ETF to trade
cash_at_risk = .5 # Percentage of cash to risk on each trade
days_prior = 3 # Number of days prior to the current date to get news
sleeptime = '24H'# Minimum time between trades
take_profit_multiplier = 0.2 # Multiplier to determine the take profit price (e.g., 20% above the last price)
stop_loss_multiplier = 0.05 # Multiplier to determine the stop loss price (e.g., 5% below the last price)
probability_threshold = 0.999  # Minimum confidence level of sentiment prediction to trigger a trade

class MLTrader(Strategy): 
    def initialize(self, symbol=symbol, cash_at_risk=cash_at_risk, sleeptime=sleeptime): 
        self.symbol = symbol
        self.sleeptime = sleeptime 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = floor(cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity

    def get_dates(self): 
        today = self.get_datetime()
        prior_date = today - Timedelta(days=days_prior)
        return today.strftime('%Y-%m-%d'), prior_date.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, prior_date = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=prior_date, end=today) 
        news = [event.__dict__['_raw']['headline'] for event in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        probability, sentiment = self.get_sentiment()

        if cash > last_price: 
            if sentiment == 'positive' and probability > probability_threshold: 
                if self.last_trade == 'sell': 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    'buy', 
                    type='bracket', 

                    # Price at which bot will sell the asset to lock in profits
                    take_profit_price=last_price*(1+take_profit_multiplier),
                    stop_loss_price=last_price*(1-stop_loss_multiplier)
                )
                self.submit_order(order) 
                self.last_trade = 'buy'
            elif sentiment == 'negative' and probability > probability_threshold: 
                if self.last_trade == 'buy': 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    'sell', 
                    type='bracket', 

                    # Price at which bot will sell the asset to lock in profits
                    take_profit_price=last_price*(1-take_profit_multiplier), 
                    stop_loss_price=last_price*(1+stop_loss_multiplier)
                )
                self.submit_order(order) 
                self.last_trade = 'sell'

broker = Alpaca(ALPACA_CREDS) 
strategy = MLTrader(name='My Strategy', 
                    broker=broker, 
                    parameters={'symbol':symbol, 'cash_at_risk':cash_at_risk})
strategy.backtest(
    YahooDataBacktesting, 
    start_date, 
    end_date, 
    parameters={'symbol':symbol, 'cash_at_risk':cash_at_risk}
)