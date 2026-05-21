"""
This is the command-line interface (CLI) for our trading bot.
It reads what the user types in the terminal, checks if it makes sense,
and sends the order to the Binance Testnet exchange.
"""

import argparse
from bot.validators import validate_order_input
from bot.orders import place_futures_order
from bot.logging_config import setup_logging

# Start our logger to save everything into the trading_bot.log file
logger = setup_logging()

def main() -> None:
    # ----------------------------------------------------
    # 1. Set up the terminal inputs (Arguments)
    # ----------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Simplified Trading Bot CLI"
    )
    
    # Define what flags the user needs to type in the terminal
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Buy or Sell")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT"], help="Type of order")
    parser.add_argument("--quantity", required=True, help="How much to trade")
    parser.add_argument("--price", required=False, default=None, help="Price (Needed for LIMIT and STOP_LIMIT)")
    parser.add_argument("--stop-price", required=False, default=None, help="Stop Trigger Price (Needed for STOP_LIMIT)")

    # Read the arguments typed by the user
    args = parser.parse_args()
    logger.info("🎬 CLI Layer invoked with user arguments.")

    # ----------------------------------------------------
    # 2. Check if user inputs are valid (Gatekeeper)
    # ----------------------------------------------------
    is_valid, error_message = validate_order_input(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=args.quantity,
        price=args.price,
        stop_price=args.stop_price
    )

    # If the inputs are wrong, print the error, log it, and stop the script
    if not is_valid:
        print(error_message)
        logger.warning(f"⚠️ Validation failed: {error_message}")
        return

    # ----------------------------------------------------
    # 3. Convert numbers from text format to decimal format
    # ----------------------------------------------------
    qty_float = float(args.quantity)
    price_float = float(args.price) if args.price else None
    stop_price_float = float(args.stop_price) if args.stop_price else None

    # Print a clean summary on the screen before sending the trade
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

    # ----------------------------------------------------
    # 4. Send the order to the Binance Exchange
    # ----------------------------------------------------
    response = place_futures_order(
        symbol=args.symbol,
        side=args.side,
        order_type=args.type,
        quantity=qty_float,
        price=price_float,
        stop_price=stop_price_float
    )
    
    # ----------------------------------------------------
    # 5. Show the exchange results on the screen
    # ----------------------------------------------------
    print("--- 🛰️ Exchange Response Details ---")
    if response and "error" not in response:
        # Get data fields. Conditional orders use 'algoId'/'algoStatus' instead of 'orderId'/'status'
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
        # If the exchange rejected it or the network failed, show the error reason
        error_reason = response.get('error', 'Unknown Error') if response else 'No Response'
        print(f"Status:       FAILED")
        print(f"Reason:       {error_reason}")
    print("------------------------------------\n")

if __name__ == "__main__":
    main()
