# Bitcoin Auto Trading Bot

A Python-based automated trading bot for Bitcoin (BTC) that implements a volatility breakout strategy using the Upbit exchange API. The bot monitors market conditions and executes trades based on technical indicators with real-time Slack notifications.

## Features

- **Volatility Breakout Strategy**: Uses the previous day's price range to calculate entry points
- **Moving Average Filter**: Incorporates 15-day moving average to confirm trend direction
- **Automated Execution**: Runs continuously with built-in error handling
- **Slack Integration**: Sends notifications for trade executions and errors
- **Daily Reset**: Automatically sells positions before market close

## Strategy Overview

The bot follows a systematic approach:

1. **Buy Condition**: Enters a position when the current price exceeds both:
   - Target price (previous close + 70% of previous day's range)
   - 15-day moving average

2. **Sell Condition**: Exits the position at the end of the trading day

3. **Position Sizing**: Uses 99.95% of available balance to account for trading fees

## Requirements
```
pyupbit
requests
```

## Configuration

Before running the bot, configure the following variables:
```python
access = "your_upbit_access_key"
secret = "your_upbit_secret_key"
myToken = "your_slack_bot_token"
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install pyupbit requests
```
3. Update API credentials in the script
4. Run the bot:
```bash
python trading_bot.py
```

## How It Works

The bot operates on a 24-hour cycle:

- **Trading Window**: Monitors the market throughout the day
- **Entry Logic**: Buys when price breaks above the target with moving average confirmation
- **Exit Logic**: Sells the entire position 10 seconds before the daily close
- **Minimum Trade**: 5,000 KRW minimum balance required for buying

## Monitoring

Check if the bot is running:
```bash
ps ax | grep .py
```

All trading activities and errors are logged to the configured Slack channel in real-time.

## Risk Disclaimer

This bot is for educational purposes. Cryptocurrency trading carries significant risk. Only trade with capital you can afford to lose. Past performance does not guarantee future results.

## Technical Details

- **Exchange**: Upbit (Korea)
- **Trading Pair**: KRW-BTC
- **Timeframe**: Daily (1D)
- **Update Interval**: 1 second
- **Fee Consideration**: 0.05% (99.95% execution)

## Notes

- The bot runs indefinitely until manually stopped
- Network connectivity is required for API calls and Slack notifications
- Ensure sufficient KRW balance before starting the bot
