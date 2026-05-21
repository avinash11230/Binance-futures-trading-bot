from binance.exceptions import BinanceAPIException
from bot.client import get_futures_client
from bot.logging_config import setup_logging

logger = setup_logging()

def place_futures_order(symbol, side, order_type, quantity, price=None, stop_price=None):
    """Sends a BUY/SELL order (MARKET, LIMIT, or STOP_LIMIT) to Binance Futures Testnet."""
    try:
        client = get_futures_client()
    except Exception as e:
        logger.error(f"❌ Failed to initialize client: {e}")
        return None

    # Translate our user-friendly "STOP_LIMIT" string to what Binance API expects: "STOP"
    binance_order_type = order_type.upper()
    if binance_order_type == "STOP_LIMIT":
        binance_order_type = "STOP"

    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": binance_order_type,
        "quantity": quantity
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"
        
    elif order_type.upper() == "STOP_LIMIT":
        params["price"] = price
        params["stopPrice"] = stop_price
        params["timeInForce"] = "GTC"

    try:
        logger.info(f"🚀 Sending {order_type} {side} order for {quantity} {symbol}...")
        response = client.futures_create_order(**params)
        logger.info(f"✅ Order Placed Successfully! Order ID: {response.get('orderId')}")
        return response
    except BinanceAPIException as e:
        logger.error(f"❌ Binance API Error: [{e.status_code}] {e.message}")
        return {"error": e.message, "status_code": e.status_code}
    except Exception as e:
        logger.error(f"⚠️ Unexpected Network Error: {e}")
        return {"error": str(e)}