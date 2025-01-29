# Trading-Bot

## Overview
- **Real-time News Analysis:** Fetches the latest news articles using the Alpaca API.
- **Sentiment Analysis:** Uses the FinBERT model to determine the sentiment of news articles.
- **Automated Trading:** Makes buy/sell decisions based on sentiment analysis.
- **Backtesting:** Uses historical data from Yahoo to test the performance of trading strategies.

Change values at the top of tradingbot.py to customize strategy nad backtesting.

## Setup
1. **Download repository:**
    ```sh
    git clone https://github.com/Rohan-Yelandur/Trading-Bot.git
    ```

2. **Create virtual environment (Windows):**
    ```sh
    python -m venv environment_namevalues
    ```

3. **Activate virtual environment:**
    ```sh
    environment_name\Scripts\activate
    ```

4. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Create a [.env](http://_vscodecontentref_/1) file** in the root directory of the project and add the following environment variables:
    ```plaintext
    API_KEY=your_api_key
    API_SECRET=your_api_secret
    BASE_URL=alpaca_url

6. **Run the bot**
    ```sh
    python tradingbot.py
    ```