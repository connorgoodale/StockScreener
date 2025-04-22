import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Value Investing Analyzer", layout="wide")

st.title("📊 Value Investing Analyzer")

st.sidebar.header("📁 Upload Financial Statements")

balance_sheet_file = st.sidebar.file_uploader("Upload Balance Sheet CSV", type=["csv"])
income_statement_file = st.sidebar.file_uploader("Upload Income Statement CSV", type=["csv"])
cash_flow_file = st.sidebar.file_uploader("Upload Cash Flow CSV", type=["csv"])
valuation_file = st.sidebar.file_uploader("Upload Valuation Metrics CSV (Optional)", type=["csv"])

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

def display_section(title, df):
    st.subheader(title)
    st.dataframe(df.style.format("{:,.2f}"), use_container_width=True)

# Load and display
dfs = {}
if balance_sheet_file:
    dfs["Balance Sheet"] = load_csv(balance_sheet_file)
if income_statement_file:
    dfs["Income Statement"] = load_csv(income_statement_file)
if cash_flow_file:
    dfs["Cash Flow Statement"] = load_csv(cash_flow_file)
if valuation_file:
    dfs["Valuation Metrics"] = load_csv(valuation_file)

# Display sections
for section, df in dfs.items():
    display_section(section, df)

# ---------------------------
# Value Investing Metrics
# ---------------------------
st.header("📈 Value Investing Analysis")

def analyze(financials):
    scores = {}

    try:
        # Extract financials
        bs = financials["Balance Sheet"]
        is_ = financials["Income Statement"]
        cf = financials["Cash Flow Statement"]
        val = financials.get("Valuation Metrics", pd.DataFrame())

        # Assume most recent year is in first column after the name col
        year_col = bs.columns[1]

        # Calculations
        total_assets = bs.loc[bs.iloc[:, 0].str.lower().str.contains("total assets"), year_col].values[0]
        total_liabilities = bs.loc[bs.iloc[:, 0].str.lower().str.contains("total liabilities"), year_col].values[0]
        total_equity = total_assets - total_liabilities
        net_income = is_.loc[is_.iloc[:, 0].str.lower().str.contains("net income"), year_col].values[0]
        revenue = is_.loc[is_.iloc[:, 0].str.lower().str.contains("total revenue"), year_col].values[0]
        operating_cash_flow = cf.loc[cf.iloc[:, 0].str.lower().str.contains("operating cash flow|net cash from operating"), year_col].values[0]
        free_cash_flow = cf.loc[cf.iloc[:, 0].str.lower().str.contains("free cash flow|capital expenditures"), year_col].values[0]

        # Ratios
        debt_to_equity = total_liabilities / total_equity
        return_on_equity = net_income / total_equity
        fcf_margin = free_cash_flow / revenue
        ocf_margin = operating_cash_flow / revenue

        scores["Debt to Equity"] = round(debt_to_equity, 2)
        scores["Return on Equity"] = round(return_on_equity, 2)
        scores["Free Cash Flow Margin"] = round(fcf_margin, 2)
        scores["Operating Cash Flow Margin"] = round(ocf_margin, 2)

        if not val.empty:
            pe = val.loc[val.iloc[:, 0].str.lower().str.contains("p/e"), year_col].values[0]
            pb = val.loc[val.iloc[:, 0].str.lower().str.contains("p/b"), year_col].values[0]
            scores["Price to Earnings (P/E)"] = round(pe, 2)
            scores["Price to Book (P/B)"] = round(pb, 2)

        return scores
    except Exception as e:
        st.error(f"❌ Error analyzing financials: {e}")
        return {}

if dfs:
    results = analyze(dfs)
    if results:
        st.success("📌 Key Financial Ratios:")
        for k, v in results.items():
            st.metric(label=k, value=v)

# Optional: weighted scoring or ranking
st.markdown("---")
st.caption("Upload additional companies to compare and create rankings.")
