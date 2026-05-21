"""
This module handles sending the trades to the Binance Futures Testnet.
It takes the clean inputs, formats them exactly how the Binance API wants them,
and processes the response or any errors that happen over the network.
"""

from typing import Any, Dict, Optional
from binance.exceptions import BinanceAPIException
from bot.client import get_futures_client
from bot.logging_config import setup_logging

# Start our logger to save everything into the trading_bot.log file
logger = setup_logging()

def place_futures_order(
    symbol: str, 
    side: str, 
    order_type: str, 
    quantity: float, 
    price: Optional[float] = None, 
    stop_price: Optional[float] = None
) -> Optional[Dict[str, Any]]:
    """Connects to the Binance API and places a market, limit, or stop-limit trade."""
    
    # ----------------------------------------------------
    # 1. Connect to the Binance Testnet client
    # ----------------------------------------------------
    try:
        client = get_futures_client()
    except Exception as e:
        logger.error(f"❌ Failed to initialize client: {e}")
        return None

    # ----------------------------------------------------
    # 2. Translate order type for the Binance API
    # ----------------------------------------------------
    # The user types "STOP_LIMIT", but the Binance API expects the word "STOP"
    binance_order_type = order_type.upper()
    if binance_order_type == "STOP_LIMIT":
        binance_order_type = "STOP"

    # Set up the basic information that every order needs
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": binance_order_type,
        "quantity": quantity
    }

    # ----------------------------------------------------
    # 3. Add extra settings based on the order type
    # ----------------------------------------------------
    # If it is a LIMIT order, we must add the execution price
    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  # GTC means 'Good Till Cancelled' (stays open until filled)
        
    # If it is a STOP_LIMIT order, we need both the trigger price and the execution price
    elif order_type.upper() == "STOP_LIMIT":
        params["price"] = price
        params["stopPrice"] = stop_price
        params["timeInForce"] = "GTC"

    # ----------------------------------------------------
    # 4. Send the trade parameters to the network
    # ----------------------------------------------------
    try:
        logger.info(f"🚀 Sending {order_type} {side} order for {quantity} {symbol}...")
        
        # Send the dictionary of options straight to the official binance library function
        response = client.futures_create_order(**params)
        
        logger.info(f"✅ Order Placed Successfully! Order ID: {response.get('orderId')}")
        return response
        
    except BinanceAPIException as e:
        # Catch errors returned directly from Binance rules (like wrong prices or bad sizes)
        logger.error(f"❌ Binance API Error: [{e.status_code}] {e.message}")
        return {"error": e.message, "status_code": e.status_code}
        
    except Exception as e:
        # Catch general connection problems like internet drops or timeout failures
        logger.error(f"⚠️ Unexpected Network Error: {e}")
        return {"error": str(e)}
