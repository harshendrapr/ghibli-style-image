import streamlit as st
import yfinance as yf

st.title("🌎 Global Stock Ticker Viewer")

ticker_input = st.text_input("Enter stock ticker (e.g. AAPL, RELIANCE.NS, MSFT, 7203.T):", "AAPL")

if st.button("Get Stock Info"):
    try:
        stock = yf.Ticker(ticker_input)
        data = stock.history(period="1d")

        if data.empty:
            st.error("No data found for ticker. Check ticker symbol.")
        else:
            st.subheader(f"{ticker_input} - Latest Close Price")
            latest_close = data['Close'].iloc[-1]
            st.metric(label="Close Price", value=f"${latest_close:.2f}")

            st.write("### Stock Info")
            info = stock.info
            st.write({
                "Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Industry": info.get("industry", "N/A"),
                "Market Cap": info.get('marketCap', "N/A"),
                "Previous Close": info.get("previousClose", "N/A"),
                "Open": info.get("open", "N/A"),
                "Day's Range": f"{info.get('dayLow', 'N/A')} - {info.get('dayHigh', 'N/A')}",
                "52 Week Range": f"{info.get('fiftyTwoWeekLow', 'N/A')} - {info.get('fiftyTwoWeekHigh', 'N/A')}",
                "Exchange": info.get("exchange", "N/A"),
                "Currency": info.get("currency", "N/A"),
            })

    except Exception as e:
        st.error(f"Error: {e}")
