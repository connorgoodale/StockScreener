# stock_grader_app.py

import streamlit as st
import yfinance as yf

# ----------------------
# SCORING FUNCTIONS
# ----------------------

def grade_growth(stock):
    try:
        revenue_growth = stock.info.get('revenueGrowth', 0)
        eps_growth = stock.info.get('earningsQuarterlyGrowth', 0)
        score = (revenue_growth + eps_growth) * 5  # max 10
        return min(max(score, 0), 10)
    except:
        return 0

def grade_valuation(stock):
    try:
        pe = stock.info.get('forwardPE', 0)
        peg = stock.info.get('pegRatio', 0)
        score = 0
        if 5 < pe < 25:
            score += 5
        if 0 < peg < 1.5:
            score += 5
        return score
    except:
        return 0

def grade_profitability(stock):
    try:
        profit_margin = stock.info.get('profitMargins', 0)
        return min(max(profit_margin * 100, 0), 10)
    except:
        return 0

def grade_momentum(stock):
    try:
        price = stock.info.get('regularMarketPrice', 0)
        target = stock.info.get('targetMeanPrice', 0)
        if price == 0:
            return 0
        diff = (target - price) / price
        return min(max(diff * 50, 0), 10)
    except:
        return 0

def grade_risk(stock):
    try:
        beta = stock.info.get('beta', 1)
        if beta < 0.8:
            return 9
        elif 0.8 <= beta <= 1.2:
            return 7
        elif 1.2 < beta <= 1.6:
            return 4
        else:
            return 2
    except:
        return 0

def letter_grade(score):
    if score >= 9: return "A+"
    elif score >= 8: return "A"
    elif score >= 7: return "B"
    elif score >= 6: return "C+"
    elif score >= 5: return "C"
    else: return "D or F"

# ----------------------
# STREAMLIT UI
# ----------------------

st.title("AI Stock Screener & Grader")
ticker_input = st.text_input("Enter stock ticker (e.g. AAPL, PLTR, TSLA)", value="PLTR")

if ticker_input:
    stock = yf.Ticker(ticker_input)
    st.subheader(f"{ticker_input.upper()} - Analysis")

    growth = grade_growth(stock)
    valuation = grade_valuation(stock)
    profitability = grade_profitability(stock)
    momentum = grade_momentum(stock)
    risk = grade_risk(stock)

    scores = {
        "Growth": growth,
        "Valuation": valuation,
        "Profitability": profitability,
        "Momentum": momentum,
        "Risk": risk
    }

    total_score = sum(scores.values()) / 5
    letter = letter_grade(total_score)

    st.markdown(f"### Final Score: **{total_score:.2f}/10.00** ({letter})")

    st.markdown("### Category Scores")
    for k, v in scores.items():
        st.progress(v / 10)
        st.write(f"{k}: {v:.2f}/10")

# ----------------------
# To run:
# ----------------------
# 1. Save this as stock_grader_app.py
# 2. In terminal: `pip install streamlit yfinance`
# 3. Run: `streamlit run stock_grader_app.py`
