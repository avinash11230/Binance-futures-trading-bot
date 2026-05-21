import streamlit as st
import json
from bot.validators import validate_order_input
from bot.orders import place_futures_order

# 1. Page Configuration & Header
st.set_page_config(page_title="Binance Futures Trader", page_icon="⚡", layout="centered")
st.title("⚡ Binance Futures Simplified Trading Desk")
st.write("An elegant graphical interface to validate and execute testnet orders securely.")

st.markdown("---")

# 2. Sidebar for Universal Configurations
st.sidebar.header("⚙️ Global Configurations")
symbol = st.sidebar.text_input("Trading Pair Symbol", value="BTCUSDT").upper()
side = st.sidebar.radio("Order Direction (Side)", options=["BUY", "SELL"])

# 3. Main Panel: Form for Order Execution
st.header("📝 Order Formulation")

# Create tabs for each order type to show clean, specific inputs
tab1, tab2, tab3 = st.tabs(["🛒 MARKET Order", "📊 LIMIT Order", "🎯 STOP_LIMIT Order"])

# Initialize default values
order_type = None
quantity = 0.0
price = None
stop_price = None

# --- MARKET TAB ---
with tab1:
    st.subheader("Market Execution")
    st.caption("Executes immediately at the best available current market price.")
    mkt_qty = st.number_input("Quantity", min_value=0.0, step=0.001, format="%.3f", key="mkt_qty")
    if st.button("🚀 Fire Market Order", type="primary"):
        order_type = "MARKET"
        quantity = mkt_qty

# --- LIMIT TAB ---
with tab2:
    st.subheader("Limit Placement")
    st.caption("Enters the order book. Triggers only when the market hits your target price.")
    lim_qty = st.number_input("Quantity", min_value=0.0, step=0.001, format="%.3f", key="lim_qty")
    lim_price = st.number_input("Limit Price ($)", min_value=0.0, step=0.1, key="lim_price")
    if st.button("📊 Submit Limit Order", type="primary"):
        order_type = "LIMIT"
        quantity = lim_qty
        price = lim_price

# --- STOP_LIMIT TAB ---
with tab3:
    st.subheader("Conditional Stop-Limit")
    st.caption("Remains hidden until the stop price is crossed, then places a limit order.")
    stop_qty = st.number_input("Quantity", min_value=0.0, step=0.001, format="%.3f", key="stop_qty")
    stop_lim_price = st.number_input("Limit Price ($)", min_value=0.0, step=0.1, key="stop_lim_price")
    stop_trig_price = st.number_input("Stop Activation Price ($)", min_value=0.0, step=0.1, key="stop_trig_price")
    if st.button("🎯 Activate Stop-Limit Order", type="primary"):
        order_type = "STOP_LIMIT"
        quantity = stop_qty
        price = stop_lim_price
        stop_price = stop_trig_price

# 4. Processing Core Logic
if order_type:
    # Trigger the validation layer
    is_valid, error_message = validate_order_input(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=str(quantity),
        price=str(price) if price else None,
        stop_price=str(stop_price) if stop_price else None
    )
    
    if not is_valid:
        st.error(error_message)
    else:
        with st.spinner("🛰️ Transmitting payload to Binance Engines..."):
            response = place_futures_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
            
        if response and "error" not in response:
            st.success("🎉 Trade Executed on Exchange Successfully!")
            
            # Dynamically handle standard vs conditional key fields
            order_id = response.get('orderId') or response.get('algoId')
            status_code = response.get('status') or response.get('algoStatus')
            
            col1, col2 = st.columns(2)
            col1.metric("Order ID", str(order_id))
            col2.metric("Status Code", str(status_code))
            
            with st.expander("🔍 View Raw JSON Receipt"):
                st.json(response)
        else:
            st.error(f"❌ Exchange Rejected: {response.get('error', 'Unknown Error')}")