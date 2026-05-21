⚡ Binance Futures Multi-Interface Trading Desk

A production-ready algorithmic trading execution application for the Binance Futures Testnet. It features a strict layered architecture and offers dual-interface access: a Command Line Interface (CLI) and a Streamlit Web Dashboard (UI).

#📁 Repository Structure

For the application to run successfully, ensure your files are organized exactly like this:

├── bot/

    │   ├── __init__.py

    │   ├── client.py

    │   ├── logging_config.py

    │   ├── orders.py

    │   └── validators.py

├── app.py

├── cli.py

├── README.md

├── requirements.txt

└── trading_bot.log


#🛠️ Setup & Installation

1. Environment Setup
Ensure you have Python 3.12+ installed.

2. Install Dependencies
pip install -r requirements.txt

3. API Key Configuration
Create a .env file in the root directory and enter the below text:
Make sure you enter your own api_key and secret_key here
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_SECRET_KEY=your_testnet_secret_key_here

#🚀 How to Run Examples

Option 1: Streamlit Web UI 🌐
Launch the interactive browser dashboard:
streamlit run app.py

Option 2: Command Line Interface (CLI) ⌨️
Run trades directly from your terminal:
MARKET Order Example:
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005

LIMIT Order Example:
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.005 --price 70000

STOP_LIMIT Order (Bonus Feature) Example:
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.005 --price 80100 --stop-price 80000



#🧠 Core Production Assumptions

API Type Translation: The frontend accepts STOP_LIMIT, but the backend execution layer automatically converts it to STOP to match the official Binance Futures API requirements.

Trigger Conditions: For a conditional BUY STOP_LIMIT order, the activation trigger (stop-price) must be set higher than the current market price to prevent immediate trigger rejection errors from the exchange.

Schema Fallbacks: Algorithmic/conditional orders return a completely distinct JSON payload schema (algoId, algoStatus) compared to standard execution orders (orderId, status). The interface layer dynamically parses both structures seamlessly.

Logging Integration: All system actions, validations, and raw exchange payloads are automatically stored in trading_bot.log using explicit UTF-8 encoding.
