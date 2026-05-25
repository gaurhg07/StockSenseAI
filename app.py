import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="StockSense AI",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# CSS LOADER
# =========================================================

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =========================================================
# HEADER
# =========================================================

st.title("📈 StockSense AI")
st.markdown("### AI-Powered Stock + CSV Financial Analyzer")

# =========================================================
# SIDEBAR
# =========================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Technical Indicators",
        "Portfolio Analyzer",
        "Correlation Analysis",
        "Risk Analysis",
        "AI Insights",
        "CSV Analyzer"
    ],
    key="nav"
)

# =========================================================
# SAFE DATA LOADER
# =========================================================

def load_stock_data(ticker, period="1y"):
    data = yf.download(ticker, period=period)

    if data.empty:
        return None

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data

# =========================================================
# CSV LOADER
# =========================================================

def load_csv(file):
    df = pd.read_csv(file)

    # Try auto-fix date column
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col])
            df = df.set_index(col)

    return df

# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.subheader("📊 Stock Dashboard")

    watchlist = ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN"]

    ticker = st.selectbox("Select Stock", watchlist)

    data = load_stock_data(ticker)

    if data is None:
        st.error("No data found for this ticker.")
        st.stop()

    data["SMA_20"] = data["Close"].rolling(20).mean()

    latest = float(data["Close"].iloc[-1])

    st.metric("Current Price", f"${latest:.2f}")

    st.line_chart(data["Close"])

# =========================================================
# TECHNICAL INDICATORS
# =========================================================

elif page == "Technical Indicators":

    st.subheader("📈 Technical Indicators")

    ticker = st.text_input("Stock", "AAPL")

    data = load_stock_data(ticker)

    if data is None:
        st.error("No data found.")
        st.stop()

    data["SMA"] = data["Close"].rolling(20).mean()
    data["EMA"] = data["Close"].ewm(span=20).mean()

    st.line_chart(data[["Close", "SMA", "EMA"]])

# =========================================================
# PORTFOLIO
# =========================================================

elif page == "Portfolio Analyzer":

    st.subheader("💼 Portfolio Analyzer")

    stocks = st.text_input("Stocks", "AAPL,MSFT,TSLA")

    stock_list = [s.strip() for s in stocks.split(",")]

    data = yf.download(stock_list, period="1y")["Close"]

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    norm = data / data.iloc[0]

    st.line_chart(norm)

# =========================================================
# CORRELATION
# =========================================================

elif page == "Correlation Analysis":

    st.subheader("🔗 Correlation")

    stocks = st.text_input("Stocks", "AAPL,MSFT,TSLA")

    stock_list = [s.strip() for s in stocks.split(",")]

    data = yf.download(stock_list, period="1y")["Close"]

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    corr = data.pct_change().corr()

    fig = px.imshow(corr, text_auto=True)

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# RISK
# =========================================================

elif page == "Risk Analysis":

    st.subheader("⚠️ Risk Analysis")

    ticker = st.text_input("Stock", "TSLA")

    data = load_stock_data(ticker)

    if data is None:
        st.error("No data found.")
        st.stop()

    returns = data["Close"].pct_change()

    vol = returns.std() * (252 ** 0.5)

    st.metric("Volatility", f"{vol:.2f}")

    st.line_chart(returns)

# =========================================================
# AI INSIGHTS
# =========================================================

elif page == "AI Insights":

    st.subheader("🤖 AI Insights")

    ticker = st.text_input("Stock", "NVDA")

    data = load_stock_data(ticker)

    if data is None:
        st.error("No data found.")
        st.stop()

    sma = data["Close"].rolling(20).mean()

    trend = "Bullish 📈" if data["Close"].iloc[-1] > sma.iloc[-1] else "Bearish 📉"

    st.success(trend)

    st.line_chart(data["Close"])

# =========================================================
# CSV ANALYZER (NEW FEATURE)
# =========================================================

elif page == "CSV Analyzer":

    st.subheader("📂 Upload Any Stock CSV")

    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file:

        df = load_csv(file)

        st.write("Preview:")
        st.dataframe(df.head())

        # Try auto detect close column
        close_col = None

        for col in df.columns:
            if "close" in col.lower():
                close_col = col

        if close_col:

            df["SMA_20"] = df[close_col].rolling(20).mean()

            st.line_chart(df[[close_col, "SMA_20"]])

        else:
            st.warning("No Close column found in CSV")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    "<center>🚀 StockSense AI | Built with Streamlit</center>",
    unsafe_allow_html=True
)
