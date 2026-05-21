def validate_order_input(symbol, side, order_type, quantity, price=None, stop_price=None):
    """
    Validates user input data types and values including STOP_LIMIT orders.
    Returns (True, None) if valid, or (False, "Error Message") if invalid.
    """
    if not symbol or not isinstance(symbol, str):
        return False, "❌ Symbol must be a valid text string (e.g., BTCUSDT)."
        
    if side.upper() not in ["BUY", "SELL"]:
        return False, "❌ Side must be exactly 'BUY' or 'SELL'."
        
    if order_type.upper() not in ["MARKET", "LIMIT", "STOP_LIMIT"]:
        return False, "❌ Order type must be 'MARKET', 'LIMIT', or 'STOP_LIMIT'."
        
    try:
        if float(quantity) <= 0:
            return False, "❌ Quantity must be greater than 0."
    except ValueError:
        return False, "❌ Quantity must be a valid number."
        
    if order_type.upper() in ["LIMIT", "STOP_LIMIT"]:
        if price is None:
            return False, f"❌ Price parameter is required for {order_type} orders."
        try:
            if float(price) <= 0:
                return False, "❌ Price must be greater than 0."
        except ValueError:
            return False, "❌ Price must be a valid number."
            
    if order_type.upper() == "STOP_LIMIT":
        if stop_price is None:
            return False, "❌ Stop Price (--stop-price) is required for STOP_LIMIT orders."
        try:
            if float(stop_price) <= 0:
                return False, "❌ Stop Price must be greater than 0."
        except ValueError:
            return False, "❌ Stop Price must be a valid number."
            
    return True, None