import argparse
from bot.validators import validate_order_input
from bot.orders import place_futures_order
from bot.logging_config import setup_logging

logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Simplified Trading Bot CLI")
    
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side (BUY or SELL)")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Amount to trade")
    parser.add_argument("--price", required=False, default=None, help="Price (Required for LIMIT/STOP_LIMIT)")
    parser.add_argument("--stop-price", required=False, default=None, help="Stop Price (Required for STOP_LIMIT)")

    args = parser.parse_args()
    logger.info("🎬 CLI Layer invoked with user arguments.")

    is_valid, error_message = validate_order_input(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price
    )

    if not is_valid:
        print(error_message)
        logger.warning(f"⚠️ Validation failed: {error_message}")
        return

    qty_float = float(args.quantity)
    price_float = float(args.price) if args.price else None
    stop_price_float = float(args.stop_price) if args.stop_price else None

    print("\n--- 📝 Order Request Summary ---")
    print(f"Symbol:     {args.symbol.upper()}")
    print(f"Side:       {args.side.upper()}")
    print(f"Type:       {args.type.upper()}")
    print(f"Quantity:   {qty_float}")
    if price_float:
        print(f"Price:      {price_float}")
    if stop_price_float:
        print(f"Stop Price: {stop_price_float}")
    print("--------------------------------\n")

    response = place_futures_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=qty_float,
        price=price_float,
        stop_price=stop_price_float
    )
    # # Temporary debug line to inspect the keys
    # print(f"DEBUG RAW RESPONSE: {response}")
    
    # 5. Display response details neatly to the user
    print("--- 🛰️ Exchange Response Details ---")
    if response and "error" not in response:
        # Check standard keys first, fall back to conditional keys if necessary
        order_id = response.get('orderId') or response.get('algoId')
        status_code = response.get('status') or response.get('algoStatus')
        executed_qty = response.get('executedQty', '0.0000')
        avg_price = response.get('avgPrice', 'N/A')

        print(f"Status:       SUCCESS")
        print(f"Order ID:     {order_id}")
        print(f"Status Code:  {status_code}")
        print(f"Executed Qty: {executed_qty}")
        print(f"Avg Price:    {avg_price}")
    else:
        print(f"Status:       FAILED")
        print(f"Reason:       {response.get('error', 'Unknown Error') if response else 'No Response'}")
    print("------------------------------------\n")

if __name__ == "__main__":
    main()