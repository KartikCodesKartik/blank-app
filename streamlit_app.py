import streamlit as st
import time
import requests
from bs4 import BeautifulSoup

# Hides the Streamlit header and menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def get_stock_price(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.select_one('.YMlKec.fxKbKc')
        if price:
            return price.text
        else:
            return None
    except Exception as e:
        return None

if __name__ == "__main__":
    st.title("Real-Time Stock Price Dashboard")

    # Initialize session state to store stocks and the no-stock message flag
    if "stocks" not in st.session_state:
        st.session_state.stocks = []
    if "no_stock_message_shown" not in st.session_state:
        st.session_state.no_stock_message_shown = False

    # Input field for user to add a stock
    stock_ticker = st.text_input("Enter Stock Ticker (e.g., IREDA:NSE):", "")

    # Button to add stock to the list
    if st.button("Add Stock"):
        if stock_ticker:
            if stock_ticker not in st.session_state.stocks:
                st.session_state.stocks.append(stock_ticker)
                st.session_state.no_stock_message_shown = False  # Reset the message flag
            else:
                st.warning(f"{stock_ticker} is already added.")
        else:
            st.error("Please enter a valid stock ticker.")

    # Display added stocks and their real-time prices
    st.subheader("Added Stocks and Prices")

    # Placeholder for stock prices
    price_placeholder = st.empty()

    # Real-time stock price updates
    while True:
        if st.session_state.stocks:
            stock_data = {}
            for ticker in st.session_state.stocks:
                url = f"https://www.google.com/finance/quote/{ticker}:NSE"
                stock_data[ticker] = get_stock_price(url)

            # Display the stock prices
            with price_placeholder.container():
                for ticker, price in stock_data.items():
                    if price:
                        st.write(f"**{ticker}**: {price}")
                    else:
                        st.write(f"**{ticker}**: Didn't find any stock of this name.")
        else:
            if not st.session_state.no_stock_message_shown:
                st.info("No stocks added yet.")
                st.session_state.no_stock_message_shown = True  # Prevent repeated messages

        time.sleep(1)  # Refresh every 2 seconds
