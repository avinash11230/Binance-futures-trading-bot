import os
from binance.client import Client
from dotenv import load_dotenv
from bot.logging_config import setup_logging

# Initialize our black-box logger
logger = setup_logging()

# Load the environment variables from the .env file
load_dotenv()

def get_futures_client():
    """Initializes and returns the Binance Futures Testnet client."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_SECRET_KEY")
    
    if not api_key or not api_secret:
        logger.error("❌ API Keys are missing! Check your .env file.")
        raise ValueError("API Keys are missing from environment.")

    logger.info("🔌 Initializing Binance Futures Testnet Client...")
    
    # Create the client and explicitly tell it to use the Testnet sandbox
    client = Client(api_key, api_secret, testnet=True)
    
    return client