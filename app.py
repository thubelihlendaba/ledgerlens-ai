import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime
import re


# ============================================================
# LEDGERLENS AI
# AI-Assisted Financial Review & Internal Control System
# ============================================================

st.set_page_config(
    page_title="LedgerLens AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL DESIGN SYSTEM
# ============================================================
# LedgerLens deliberately uses its own dark branded interface.
# This prevents Streamlit Light/System/Dark preferences from
# materially changing the appearance seen by reviewers.
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL APPLICATION
   ========================================================= */

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stApp {
    background-color: #0E1117 !important;
    color: #F7F9FC !important;
}

[data-testid="stMainBlockContainer"] {
    background-color: #0E1117 !important;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1500px !important;
}

/* Default text */

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp li,
.stApp div {
    color: #F7F9FC;
}

h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF !important;
}

hr {
    border-color: #293746 !important;
}


/* =========================================================
   STREAMLIT TOP BAR
   ========================================================= */

[data-testid="stHeader"] {
    background-color: #0E1117 !important;
}

[data-testid="stToolbar"] {
    background-color: #0E1117 !important;
}

[data-testid="stDecoration"] {
    background-color: #0E1117 !important;
}

[data-testid="stToolbar"] button,
[data-testid="stToolbar"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

[data-testid="stHeaderActionElements"] {
    color: #FFFFFF !important;
}

header[data-testid="stHeader"] {
    border-bottom: 1px solid #1D2A36 !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background-color: #0B2F4A !important;
    border-right: 1px solid #21445E !important;
}

[data-testid="stSidebar"] > div {
    background-color: #0B2F4A !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] hr {
    border-color: #315068 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding-top: 2px !important;
    padding-bottom: 2px !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #A9C0D2 !important;
}


/* =========================================================
   MAIN LEDGERLENS HEADER
   ========================================================= */

.main-header {
    background: linear-gradient(135deg, #15466B 0%, #28688F 100%);
    padding: 30px 36px;
    border-radius: 0 0 16px 16px;
    margin-bottom: 30px;
    color: #FFFFFF !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.20);
}

.main-header * {
    color: #FFFFFF !important;
}

.main-header h1 {
    margin: 15px 0 8px 0 !important;
    font-size: 42px !important;
    line-height: 1.15 !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

.main-header p {
    margin: 0 !important;
    font-size: 16px !important;
    color: #E6F1F8 !important;
    opacity: 1 !important;
}

.header-kicker {
    font-size: 13px;
    letter-spacing: 3px;
    font-weight: 800;
    color: #FFFFFF !important;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    font-size: 23px;
    line-height: 1.25;
    font-weight: 800;
    color: #54B4E6 !important;
    margin-top: 8px;
    margin-bottom: 18px;
}

.subtle-text {
    color: #A8B5C2 !important;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

[data-testid="stMetric"] {
    background-color: #111A23 !important;
    border: 1px solid #2A3A48 !important;
    border-radius: 12px !important;
    padding: 17px 17px 15px 17px !important;
    min-height: 102px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.10);
}

[data-testid="stMetricLabel"] {
    color: #D6DEE6 !important;
}

[data-testid="stMetricLabel"] p {
    color: #D6DEE6 !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

[data-testid="stMetricValue"] div {
    color: #FFFFFF !important;
}


/* =========================================================
   TEXT INPUT / SEARCH
   ========================================================= */

div[data-baseweb="input"] {
    background-color: #111A23 !important;
    border: 1px solid #5A6A78 !important;
    border-radius: 8px !important;
}

div[data-baseweb="input"] input {
    background-color: #111A23 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

div[data-baseweb="input"] input::placeholder {
    color: #B9C4CE !important;
    -webkit-text-fill-color: #B9C4CE !important;
    opacity: 1 !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #54B4E6 !important;
    box-shadow: 0 0 0 1px #54B4E6 !important;
}


/* =========================================================
   SELECT BOXES
   ========================================================= */

div[data-baseweb="select"] > div {
    background-color: #111A23 !important;
    border-color: #425465 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="select"] span {
    color: #FFFFFF !important;
}


/* =========================================================
   DATAFRAMES
   ========================================================= */

/*
   Streamlit dataframes use their own rendering layer.
   We intentionally retain a light "working-paper" data surface
   because it creates strong contrast against the dark interface.
*/

[data-testid="stDataFrame"] {
    border: 1px solid #425465 !important;
    border-radius: 10px !important;
    background: #F7F9FC !important;
}

/* Keep Streamlit's native dataframe toolbar accessible.
   This preserves fullscreen/expand and other table controls. */
[data-testid="stDataFrame"] iframe {
    border-radius: 10px !important;
}

[data-testid="stDataFrame"] [data-testid="stElementToolbar"] {
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 1000 !important;
}


/* =========================================================
   TEXT AREA / MANAGEMENT REPORT
   ========================================================= */

div[data-baseweb="textarea"] {
    background-color: #111A23 !important;
    border-radius: 10px !important;
}

div[data-baseweb="textarea"] textarea,
textarea {
    background-color: #111A23 !important;
    color: #F7F9FC !important;
    -webkit-text-fill-color: #F7F9FC !important;
    border: 1px solid #425465 !important;
    border-radius: 10px !important;
    font-family: "Courier New", monospace !important;
    line-height: 1.55 !important;
}

div[data-baseweb="textarea"] textarea::placeholder {
    color: #AAB7C3 !important;
    opacity: 1 !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #54B4E6 !important;
}


/* =========================================================
   PRIMARY BUTTONS
   ========================================================= */

.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(90deg, #E94B50, #FF555A) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
    min-height: 44px !important;
}

.stButton > button[kind="primary"] *,
.stButton > button[data-testid="stBaseButton-primary"] * {
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #D94046 !important;
    color: #FFFFFF !important;
}


/* =========================================================
   DOWNLOAD BUTTONS
   ========================================================= */

.stDownloadButton > button {
    background: linear-gradient(90deg, #E94B50, #FF555A) !important;
    color: #FFFFFF !important;
    border: 1px solid #FF555A !important;
    border-radius: 8px !important;
    font-weight: 750 !important;
    min-height: 46px !important;
    width: 100% !important;
}

.stDownloadButton > button p,
.stDownloadButton > button span,
.stDownloadButton > button div {
    color: #FFFFFF !important;
}

.stDownloadButton > button:hover {
    background: #D94046 !important;
    border-color: #D94046 !important;
    color: #FFFFFF !important;
}

.stDownloadButton > button:hover p,
.stDownloadButton > button:hover span,
.stDownloadButton > button:hover div {
    color: #FFFFFF !important;
}


/* =========================================================
   INFORMATION BOXES
   ========================================================= */

.info-box {
    padding: 18px 20px;
    border-radius: 11px;
    background-color: #132536;
    border-left: 5px solid #2999D5;
    margin: 16px 0 20px 0;
    color: #E8F0F6 !important;
}

.info-box * {
    color: #E8F0F6 !important;
}

.warning-box {
    padding: 18px 20px;
    border-radius: 11px;
    background-color: #2A2114;
    border-left: 5px solid #E5A23B;
    margin: 16px 0 20px 0;
}

.warning-box,
.warning-box * {
    color: #F6E7C8 !important;
}

.success-box {
    padding: 18px 20px;
    border-radius: 11px;
    background-color: #122A22;
    border-left: 5px solid #35A46F;
    margin: 16px 0 20px 0;
}

.success-box,
.success-box * {
    color: #DDF4E8 !important;
}


/* =========================================================
   STREAMLIT ALERTS
   ========================================================= */

[data-testid="stAlert"] {
    border-radius: 10px !important;
}

[data-testid="stAlert"] p {
    color: inherit !important;
}


/* =========================================================
   PROGRESS BAR
   ========================================================= */

[data-testid="stProgress"] > div > div > div > div {
    background-color: #2999D5 !important;
}


/* =========================================================
   AI REVIEW CONTAINER
   ========================================================= */

.ai-review-label {
    margin-top: 28px;
    margin-bottom: 10px;
    color: #54B4E6 !important;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.ai-notice {
    background-color: #111A23;
    border: 1px solid #293B4A;
    border-radius: 10px;
    padding: 16px 18px;
    margin: 15px 0 20px 0;
}

.ai-notice,
.ai-notice * {
    color: #DCE5ED !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    color: #91A2B1 !important;
    font-size: 12px;
    line-height: 1.8;
    padding-top: 38px;
    padding-bottom: 10px;
}

.footer * {
    color: #91A2B1 !important;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .main-header {
        padding: 24px;
    }

    .main-header h1 {
        font-size: 34px !important;
    }

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


@st.cache_data
def load_csv(filename):
    path = BASE_DIR / filename

    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def find_column(df, possible_names):
    if df.empty:
        return None

    normalized = {
        str(col).strip().lower().replace(" ", "_"): col
        for col in df.columns
    }

    for name in possible_names:
        key = name.strip().lower().replace(" ", "_")

        if key in normalized:
            return normalized[key]

    return None


def money(value):
    try:
        value = float(value)

        if value < 0:
            return f"(${abs(value):,.2f})"

        return f"${value:,.2f}"

    except Exception:
        return "$0.00"


def numeric_series(df, column):
    if column is None or df.empty:
        return pd.Series(dtype=float)

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


def pretty_column_name(column):
    replacements = {
        "Transaction_ID": "Transaction ID",
        "Vendor_or_Client": "Vendor / Client",
        "Transaction_Type": "Transaction Type",
        "Net_Income": "Net Income",
        "Profit_Margin": "Profit Margin",
        "Risk_Score": "Risk Score",
        "Risk_Level": "Risk Level",
        "Signal_Count": "Signal Count",
        "Reconciliation_Status": "Reconciliation Status",
        "Review_Reason": "Review Reason",
        "Bank_Reference": "Bank Reference",
        "Bank_Date": "Bank Date",
        "Bank_Description": "Bank Description",
        "Bank_Amount": "Bank Amount",
        "Anomaly_ID": "Anomaly ID",
        "Anomaly_Type": "Anomaly Type",
        "Evaluation_Result": "Evaluation Result",
    }

    if column in replacements:
        return replacements[column]

    return str(column).replace("_", " ")


def clean_display_dataframe(df):
    """
    Creates a presentation-only copy.
    Underlying analytical data is never changed.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    display_df = df.copy()

    # Replace missing display values with an em dash.
    display_df = display_df.where(
        pd.notna(display_df),
        "—"
    )

    display_df = display_df.rename(
        columns={
            col: pretty_column_name(col)
            for col in display_df.columns
        }
    )

    return display_df


def financial_dataframe(df):
    """
    Formats financial summary tables for presentation.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    display_df = df.copy()

    for col in display_df.columns:

        normalized = str(col).lower()

        if any(
            keyword in normalized
            for keyword in [
                "revenue",
                "expense",
                "net_income",
                "net income",
                "amount",
            ]
        ):
            numeric = pd.to_numeric(
                display_df[col],
                errors="coerce"
            )

            if numeric.notna().any():
                display_df[col] = numeric.map(
                    lambda x:
                    money(x)
                    if pd.notna(x)
                    else "—"
                )

        if "margin" in normalized:
            numeric = pd.to_numeric(
                display_df[col],
                errors="coerce"
            )

            if numeric.notna().any():
                display_df[col] = numeric.map(
                    lambda x:
                    f"{x:.2f}%"
                    if pd.notna(x)
                    else "—"
                )

        if normalized in ["month", "period"]:

            def format_month(value):
                try:
                    parsed = pd.to_datetime(
                        str(value),
                        format="%Y-%m"
                    )
                    return parsed.strftime("%b %Y")
                except Exception:
                    return value

            display_df[col] = display_df[col].map(
                format_month
            )

    return clean_display_dataframe(display_df)


def transaction_dataframe(df):
    """
    Formats transaction tables without changing source data.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    display_df = df.copy()

    amount_columns = [
        col
        for col in display_df.columns
        if "amount" in str(col).lower()
    ]

    for col in amount_columns:

        numeric = pd.to_numeric(
            display_df[col],
            errors="coerce"
        )

        if numeric.notna().any():

            display_df[col] = [
                money(value)
                if pd.notna(value)
                else "—"
                for value in numeric
            ]

    return clean_display_dataframe(display_df)


def dataframe_height(df, max_rows=16):
    if df is None or df.empty:
        return 180

    rows = min(len(df), max_rows)

    return max(
        180,
        38 + rows * 35
    )


def render_dataframe(df, height=None):
    if df is None or df.empty:
        return

    if height is None:
        height = dataframe_height(df)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=height,
    )

def clean_ai_markdown(text):
    """
    Cleans common formatting artifacts returned by generative models
    without changing the substantive AI review.
    """

    if not text:
        return ""

    cleaned = str(text)

    # Repair cases where model markdown attaches directly to currency.
    cleaned = re.sub(
        r"\$([0-9,]+\.\d{2})\s*\*\*",
        r"$\1",
        cleaned
    )

    cleaned = cleaned.replace("\\$", "$")

    # Remove accidental duplicated bold markers around currency.
    cleaned = re.sub(
        r"\*\*\s*(\$[0-9,]+\.\d{2})\s*\*\*",
        r"**\1**",
        cleaned
    )

    # Prevent excessive blank lines.
    cleaned = re.sub(
        r"\n{4,}",
        "\n\n\n",
        cleaned
    )

    return cleaned.strip()



# ============================================================
# LOAD LEDGERLENS DATA
# ============================================================

transactions = load_csv("transactions.csv")
clean_transactions = load_csv("clean_transactions.csv")
monthly_summary = load_csv("monthly_summary.csv")
review_queue = load_csv("review_queue.csv")
transaction_risk = load_csv("transaction_risk.csv")
unmatched_items = load_csv("unmatched_items.csv")
ground_truth = load_csv("ground_truth.csv")
evaluation_results = load_csv("evaluation_results.csv")
evaluation_summary = load_csv("evaluation_summary.csv")
project_metadata = load_csv("project_metadata.csv")


# ============================================================
# FINANCIAL METRICS
# ============================================================

revenue = 0.0
expenses = 0.0
net_income = 0.0

rev_col = find_column(
    monthly_summary,
    ["Revenue", "Total_Revenue"]
)

exp_col = find_column(
    monthly_summary,
    ["Expenses", "Expense", "Total_Expenses"]
)

net_col = find_column(
    monthly_summary,
    ["Net_Income", "Net Income", "Profit"]
)

if rev_col:
    revenue = numeric_series(
        monthly_summary,
        rev_col
    ).sum()

if exp_col:
    expenses = numeric_series(
        monthly_summary,
        exp_col
    ).sum()

if net_col:
    net_income = numeric_series(
        monthly_summary,
        net_col
    ).sum()
else:
    net_income = revenue - expenses


# ============================================================
# FALLBACK FINANCIAL CALCULATION
# ============================================================

if revenue == 0 and not clean_transactions.empty:

    amount_col = find_column(
        clean_transactions,
        ["Amount"]
    )

    type_col = find_column(
        clean_transactions,
        [
            "Transaction_Type",
            "Transaction Type",
            "Type"
        ]
    )

    if amount_col and type_col:

        types = (
            clean_transactions[type_col]
            .astype(str)
            .str.lower()
        )

        revenue = pd.to_numeric(
            clean_transactions.loc[
                types.str.contains(
                    "revenue|income",
                    regex=True
                ),
                amount_col
            ],
            errors="coerce"
        ).sum()

        expenses = abs(
            pd.to_numeric(
                clean_transactions.loc[
                    types.str.contains(
                        "expense",
                        regex=True
                    ),
                    amount_col
                ],
                errors="coerce"
            ).sum()
        )

        net_income = revenue - expenses


# ============================================================
# CONTROL / RISK METRICS
# ============================================================

# IMPORTANT:
# The complete source ledger is the reviewed population.
# This preserves the project's 687-transaction population.
transactions_reviewed = len(transactions)

if transactions_reviewed == 0:
    transactions_reviewed = len(clean_transactions)


unique_flagged = len(transaction_risk)

priority_col = find_column(
    transaction_risk,
    [
        "Priority",
        "Risk_Level",
        "Risk Level"
    ]
)

if priority_col:

    priority_values = (
        transaction_risk[priority_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    high_count = int(
        (priority_values == "high").sum()
    )

    medium_count = int(
        (priority_values == "medium").sum()
    )

    low_count = int(
        (priority_values == "low").sum()
    )

else:

    high_count = 0
    medium_count = 0
    low_count = 0


matched_transactions = max(
    transactions_reviewed - len(unmatched_items),
    0
)

if transactions_reviewed > 0:

    reconciliation_rate = (
        matched_transactions
        / transactions_reviewed
    ) * 100

else:

    reconciliation_rate = 0.0


# ============================================================
# GROUND-TRUTH EVALUATION
# ============================================================

known_anomalies = len(ground_truth)

detected_anomalies = 0

detected_col = find_column(
    evaluation_results,
    ["Detected"]
)

result_col = find_column(
    evaluation_results,
    [
        "Evaluation_Result",
        "Result"
    ]
)

if detected_col:

    detected_anomalies = int(
        evaluation_results[detected_col]
        .astype(str)
        .str.lower()
        .isin([
            "true",
            "1",
            "yes",
            "detected"
        ])
        .sum()
    )

elif result_col:

    detected_anomalies = int(
        evaluation_results[result_col]
        .astype(str)
        .str.lower()
        .eq("detected")
        .sum()
    )


missed_anomalies = max(
    known_anomalies - detected_anomalies,
    0
)

if known_anomalies > 0:

    detection_rate = (
        detected_anomalies
        / known_anomalies
    ) * 100

else:

    detection_rate = 0.0


# ============================================================
# SESSION STATE
# ============================================================

if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🔎 LedgerLens AI")

    st.caption(
        "AI-assisted financial control and management review"
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Financial Performance",
            "Risk Review",
            "Transaction Explorer",
            "Reconciliation",
            "Model Evaluation",
            "AI Management Review",
            "Management Report",
            "System Design",
        ],
    )

    st.markdown("---")

    st.caption("Lakeview Consulting LLC")
    st.caption("January – June 2026")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """<div class="main-header"><div class="header-kicker">AI-ASSISTED FINANCIAL REVIEW</div><h1>LedgerLens AI</h1><p>Financial controls • anomaly detection • reconciliation • risk prioritization • AI-assisted management interpretation</p></div>""",
    unsafe_allow_html=True,
)

# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.markdown(
        '<div class="section-title">Executive Dashboard</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Revenue",
        money(revenue)
    )

    c2.metric(
        "Expenses",
        money(expenses)
    )

    c3.metric(
        "Net Income",
        money(net_income)
    )

    c4.metric(
        "Reconciliation",
        f"{reconciliation_rate:.2f}%"
    )

    st.markdown("### Transaction Review")

    a, b, c, d = st.columns(4)

    a.metric(
        "Transactions Reviewed",
        f"{transactions_reviewed:,}"
    )

    b.metric(
        "Unique Transactions Flagged",
        f"{unique_flagged:,}"
    )

    c.metric(
        "High Priority",
        f"{high_count:,}"
    )

    d.metric(
        "Unmatched Transactions",
        f"{len(unmatched_items):,}"
    )

    st.markdown("---")

    st.markdown("### Risk Distribution")

    risk_df = pd.DataFrame(
        {
            "Priority": [
                "High",
                "Medium",
                "Low"
            ],
            "Transactions": [
                high_count,
                medium_count,
                low_count
            ],
        }
    )

    fig = px.bar(
        risk_df,
        x="Priority",
        y="Transactions",
        text="Transactions",
        title="Transactions Requiring Management Review",
    )

    fig.update_traces(
        marker_color="#54B4E6",
        textposition="outside",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="#F7F9FC",
        title_font_color="#FFFFFF",
        xaxis_title="Risk Priority",
        yaxis_title="Transactions",
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
<div class="info-box">
<b>Review interpretation:</b>
Flagged transactions represent items requiring human verification.
A LedgerLens alert does not independently establish fraud,
misconduct, or accounting error.
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FINANCIAL PERFORMANCE
# ============================================================

elif page == "Financial Performance":

    st.markdown(
        '<div class="section-title">Financial Performance</div>',
        unsafe_allow_html=True,
    )

    if monthly_summary.empty:

        st.warning(
            "Monthly financial summary data is unavailable."
        )

    else:

        financial_display = financial_dataframe(
            monthly_summary
        )

        render_dataframe(
            financial_display,
            height=dataframe_height(
                financial_display,
                max_rows=10
            )
        )

        month_col = find_column(
            monthly_summary,
            [
                "Month",
                "Date",
                "Period"
            ]
        )

        chart_columns = [
            col
            for col in [
                rev_col,
                exp_col,
                net_col
            ]
            if col is not None
        ]

        if month_col and chart_columns:

            chart_df = monthly_summary[
                [month_col] + chart_columns
            ].copy()

            chart_df = chart_df.melt(
                id_vars=month_col,
                value_vars=chart_columns,
                var_name="Financial Metric",
                value_name="Amount",
            )

            chart_df[
                "Financial Metric"
            ] = chart_df[
                "Financial Metric"
            ].map(pretty_column_name)

            fig = px.line(
                chart_df,
                x=month_col,
                y="Amount",
                color="Financial Metric",
                markers=True,
                title="Monthly Financial Performance",
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117",
                font_color="#F7F9FC",
                title_font_color="#FFFFFF",
                xaxis_title="Month",
                yaxis_title="Amount ($)",
                legend_title="Metric",
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.markdown("### Period Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Revenue",
        money(revenue)
    )

    c2.metric(
        "Total Expenses",
        money(expenses)
    )

    c3.metric(
        "Net Income",
        money(net_income)
    )


# ============================================================
# RISK REVIEW
# ============================================================

elif page == "Risk Review":

    st.markdown(
        '<div class="section-title">Risk Review</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
LedgerLens aggregates individual control signals into
transaction-level risk scores so management can focus on
transactions requiring the most attention.
"""
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "High Priority",
        high_count
    )

    c2.metric(
        "Medium Priority",
        medium_count
    )

    c3.metric(
        "Low Priority",
        low_count
    )

    c4.metric(
        "Total Flagged",
        unique_flagged
    )

    if transaction_risk.empty:

        st.warning(
            "Transaction risk data is unavailable."
        )

    else:

        selected_priority = st.selectbox(
            "Filter by priority",
            [
                "All",
                "High",
                "Medium",
                "Low"
            ],
        )

        risk_display = transaction_risk.copy()

        if (
            selected_priority != "All"
            and priority_col is not None
        ):

            risk_display = risk_display[
                risk_display[priority_col]
                .astype(str)
                .str.lower()
                == selected_priority.lower()
            ]

        risk_display = transaction_dataframe(
            risk_display
        )

        render_dataframe(
            risk_display,
            height=500
        )

    st.markdown(
        """
<div class="info-box">
Risk scores prioritize review effort. They are control indicators,
not independent conclusions that a transaction is improper.
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# TRANSACTION EXPLORER
# ============================================================

elif page == "Transaction Explorer":

    st.markdown(
        '<div class="section-title">Transaction Explorer</div>',
        unsafe_allow_html=True,
    )

    source_df = (
        clean_transactions.copy()
        if not clean_transactions.empty
        else transactions.copy()
    )

    if source_df.empty:

        st.warning(
            "Transaction data is unavailable."
        )

    else:

        search = st.text_input(
            "Search transactions",
            placeholder=(
                "Search by transaction ID, vendor, category, "
                "description, amount, or transaction type..."
            ),
        )

        filtered = source_df.copy()

        if search:

            mask = (
                filtered
                .astype(str)
                .apply(
                    lambda column:
                    column.str.contains(
                        search,
                        case=False,
                        na=False
                    )
                )
                .any(axis=1)
            )

            filtered = filtered[mask]

        st.caption(
            f"{len(filtered):,} transactions displayed"
        )

        transaction_display = transaction_dataframe(
            filtered
        )

        render_dataframe(
            transaction_display,
            height=500
        )


# ============================================================
# RECONCILIATION
# ============================================================

elif page == "Reconciliation":

    st.markdown(
        '<div class="section-title">Bank Reconciliation</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Matched Transactions",
        f"{matched_transactions:,}"
    )

    c2.metric(
        "Unmatched Transactions",
        f"{len(unmatched_items):,}"
    )

    c3.metric(
        "Reconciliation Rate",
        f"{reconciliation_rate:.2f}%"
    )

    st.progress(
        min(
            max(
                reconciliation_rate / 100,
                0
            ),
            1
        )
    )

    st.markdown("### Unmatched Items")

    if unmatched_items.empty:

        st.success(
            "No unmatched transactions were identified."
        )

    else:

        unmatched_display = transaction_dataframe(
            unmatched_items
        )

        render_dataframe(
            unmatched_display,
            height=dataframe_height(
                unmatched_display,
                max_rows=10
            )
        )

        st.markdown(
            """
<div class="info-box">
<b>Follow-up:</b>
Unmatched items require review against subsequent bank activity
or supporting documentation. Timing differences may explain
legitimate unmatched entries.
</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# MODEL EVALUATION
# ============================================================

elif page == "Model Evaluation":

    st.markdown(
        '<div class="section-title">'
        'Independent Ground-Truth Validation'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Known Anomalies",
        known_anomalies
    )

    c2.metric(
        "Detected",
        int(detected_anomalies)
    )

    c3.metric(
        "Missed",
        int(missed_anomalies)
    )

    c4.metric(
        "Detection Rate",
        f"{detection_rate:.1f}%"
    )

    st.markdown(
        """
<div class="info-box">

<b>Validation methodology</b><br><br>

The ground-truth dataset contains intentionally embedded anomalies
used to evaluate LedgerLens after deterministic financial-control
and risk-scoring processes have been applied.

This is a <b>synthetic benchmark</b> and should not be interpreted
as universal real-world anomaly-detection accuracy.

</div>
""",
        unsafe_allow_html=True,
    )

    if not evaluation_results.empty:

        st.markdown(
            "### Transaction-Level Evaluation"
        )

        evaluation_display = transaction_dataframe(
            evaluation_results
        )

        render_dataframe(
            evaluation_display,
            height=500
        )

    if not evaluation_summary.empty:

        st.markdown(
            "### Evaluation Summary"
        )

        evaluation_summary_display = (
            clean_display_dataframe(
                evaluation_summary
            )
        )

        render_dataframe(
            evaluation_summary_display,
            height=dataframe_height(
                evaluation_summary_display,
                max_rows=12
            )
        )


# ============================================================
# AI MANAGEMENT REVIEW
# ============================================================

elif page == "AI Management Review":

    st.markdown(
        '<div class="section-title">'
        'Gemini-Assisted Management Review'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
LedgerLens performs deterministic financial controls,
reconciliation, anomaly identification, and risk prioritization
**before** generative AI is used.

Gemini serves as an **interpretation and communication layer**,
converting verified analytical results into a management-oriented
financial and internal-control review.

The generative AI layer does not independently classify a
transaction as fraud, misconduct, or a confirmed accounting error.
"""
    )

    st.markdown(
        "### Verified Analytical Context"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Net Income",
        money(net_income)
    )

    c2.metric(
        "Flagged Transactions",
        unique_flagged
    )

    c3.metric(
        "High Priority",
        high_count
    )

    c4.metric(
        "Reconciliation",
        f"{reconciliation_rate:.2f}%"
    )

    if st.button(
        "✨ Generate AI Management Review",
        type="primary",
        use_container_width=True,
    ):

        try:

            from google import genai

            api_key = st.secrets.get(
                "GEMINI_API_KEY",
                ""
            )

            model_name = st.secrets.get(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            )

            if not api_key:

                st.error(
                    "Gemini API key has not been configured "
                    "in Streamlit Secrets."
                )

            else:

                client = genai.Client(
                    api_key=api_key
                )

                risk_context = (
                    transaction_risk
                    .head(30)
                    .to_string(index=False)
                    if not transaction_risk.empty
                    else "No transaction risk records available."
                )

                unmatched_context = (
                    unmatched_items
                    .head(15)
                    .to_string(index=False)
                    if not unmatched_items.empty
                    else "No unmatched transactions."
                )

                evaluation_context = (
                    evaluation_results
                    .head(30)
                    .to_string(index=False)
                    if not evaluation_results.empty
                    else "No evaluation records available."
                )

                system_instructions = """
You are the generative AI review layer of LedgerLens AI,
an AI-assisted financial review and internal-control system.

LedgerLens has already performed deterministic financial
analytics, transaction-level control tests, reconciliation,
anomaly detection, risk prioritization, and independent
synthetic validation.

Your responsibility is to interpret those VERIFIED findings
for management.

STRICT RULES:

1. Use ONLY information contained in the supplied
   LedgerLens verified context.

2. Do not invent transactions, vendors, amounts, dates,
   explanations, financial results, or control findings.

3. Do not independently recalculate financial metrics.
   Treat supplied LedgerLens calculations as the verified
   analytical source.

4. Never describe a flagged transaction as fraud,
   misconduct, or a confirmed accounting error unless the
   supplied evidence explicitly establishes that conclusion.

5. Clearly distinguish:
   - detected anomalies,
   - items requiring human review,
   - reconciliation exceptions,
   - and confirmed factual results.

6. Prioritize findings using the supplied LedgerLens risk
   information.

7. Explain WHY significant findings matter instead of simply
   repeating that they were flagged.

8. Provide practical and specific management follow-up
   procedures.

9. Mention positive control results where relevant,
   including successful reconciliation performance.

10. Make clear that the ground-truth detection result is based
    on intentionally embedded anomalies in a synthetic dataset
    and is not evidence of universal real-world accuracy.

11. FORMATTING RULES — FOLLOW EXACTLY:

    Use Markdown ONLY for the six required section headings
    beginning with ##.

    Do NOT use Markdown bold or italics anywhere in the body.
    Do NOT use *, **, _, or __ for emphasis.

    Write all body paragraphs in plain text.

    When listing individual findings, use normal Markdown
    bullet points beginning with "- " only.

    Currency values must contain no spaces and must use
    standard U.S. formatting.

    CORRECT:
    $741,774.90
    $320,880.41
    $5,000.00
    $4,850.00
    $224.90

    INCORRECT:
    $741, 774.90
    $5, 000.00
    $ 5,000.00
    5,000.00
    $741,774.90**
    **$741,774.90**

    Dates must use YYYY-MM-DD format.

    Write multiplication comparisons as normal plain text.

    CORRECT:
    22.2 times the vendor's historical median of $224.90

    INCORRECT:
    22.2timesthevendor'shistoricalmedianof224.90
    *22.2 times the vendor's historical median of $224.90*

    A transaction finding should follow this format:

    - Amazon Business (RND001, 2026-03-11, $5,000.00):
      This payment is 22.2 times the vendor's historical
      median of $224.90. The transaction requires review
      of supporting documentation.

    Never place Markdown formatting characters next to
    transaction names, dates, numbers, percentages, or
    currency values.

12. Write in a concise, professional financial-review style
    suitable for management.

Use exactly these sections:

## 1. Executive Summary
## 2. Financial Performance
## 3. Key Review Findings
## 4. Reconciliation and Controls
## 5. Recommended Management Actions
## 6. Conclusion
"""

                management_prompt = f"""
Prepare a management-level financial and internal-control review
for Lakeview Consulting LLC for January 1, 2026 through
June 30, 2026.

The information below was produced by the LedgerLens deterministic
financial analytics and control engine.

You are NOT being asked to independently discover anomalies.
Interpret, explain, prioritize, and communicate the verified
findings.

================ VERIFIED LEDGERLENS CONTEXT ================

FINANCIAL PERFORMANCE

Revenue: {money(revenue)}
Operating expenses: {money(expenses)}
Net income: {money(net_income)}

CONTROL REVIEW

Transactions reviewed: {transactions_reviewed:,}
Unique transactions flagged: {unique_flagged:,}
High priority: {high_count:,}
Medium priority: {medium_count:,}
Low priority: {low_count:,}

BANK RECONCILIATION

Matched transactions: {matched_transactions:,}
Unmatched transactions: {len(unmatched_items):,}
Reconciliation rate: {reconciliation_rate:.2f}%

SYNTHETIC GROUND-TRUTH EVALUATION

Known intentionally embedded anomalies: {known_anomalies:,}
Detected anomalies: {detected_anomalies:,}
Missed anomalies: {missed_anomalies:,}
Synthetic benchmark detection rate: {detection_rate:.1f}%

TRANSACTION RISK FINDINGS

{risk_context}

UNMATCHED RECONCILIATION ITEMS

{unmatched_context}

GROUND-TRUTH EVALUATION DETAIL

{evaluation_context}

==============================================================

Your review should:

- explain overall financial performance and profitability;
- identify the most important high-priority review items;
- explain why unusual amounts warrant substantiation;
- discuss possible duplicate transactions and verification steps;
- discuss category inconsistencies and financial-reporting impact;
- discuss material new vendors and vendor due diligence;
- discuss large round-dollar transactions and documentation;
- explain reconciliation performance and unmatched items;
- distinguish analytical flags from confirmed errors;
- provide specific practical actions management should take;
- recognize positive control results;
- clearly state the limitation of synthetic validation.

Do not imply that Gemini performed the underlying financial
analysis. LedgerLens performed the deterministic analytics and
controls. Gemini provides management interpretation and narrative
synthesis of those verified results.

{system_instructions}
"""

                with st.spinner(
                    "Gemini is preparing the management review..."
                ):

                    response = (
                        client.models.generate_content(
                            model=model_name,
                            contents=management_prompt,
                        )
                    )

                raw_review = (
                    response.text
                    if response.text
                    else ""
                )

                st.session_state.ai_review = (
                    clean_ai_markdown(raw_review)
                    if raw_review
                    else "No review was returned."
                )

        except Exception as error:

            st.error(
                "AI review could not be generated. "
                f"Details: {error}"
            )

    if st.session_state.ai_review:

        st.markdown("---")

        st.markdown(
            '<div class="ai-review-label">'
            'Generated Management Interpretation'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
<div class="ai-notice">
The narrative below was prepared by Gemini using verified
LedgerLens analytical outputs. Deterministic calculations,
control testing, risk scoring, reconciliation, and synthetic
validation remain the responsibility of the LedgerLens
analytical engine.
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            clean_ai_markdown(
                st.session_state.ai_review
            )
        )

        st.download_button(
            "⬇️ Download AI Management Review",
            data=st.session_state.ai_review,
            file_name=(
                "LedgerLens_AI_Management_Review.txt"
            ),
            mime="text/plain",
            type="primary",
            use_container_width=True,
        )

    else:

        st.markdown(
            """
<div class="info-box">
Select <b>Generate AI Management Review</b> to convert the
verified LedgerLens analytical results into a management-oriented
financial and internal-control review.
</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# MANAGEMENT REPORT
# ============================================================

elif page == "Management Report":

    st.markdown(
        '<div class="section-title">'
        'Management Report'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
This section consolidates LedgerLens financial results,
control findings, reconciliation results, independent
synthetic validation, and AI-assisted interpretation into
a management-ready summary.
"""
    )

    ai_report_section = (
        st.session_state.ai_review
        if st.session_state.ai_review
        else (
            "AI management review has not yet been generated. "
            "Open the AI Management Review page and select "
            "'Generate AI Management Review' to include the "
            "Gemini-assisted interpretation."
        )
    )

    report_text = f"""LEDGERLENS AI
MANAGEMENT REVIEW REPORT

Lakeview Consulting LLC
Reporting Period: January 1, 2026 - June 30, 2026

Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

============================================================
EXECUTIVE FINANCIAL SUMMARY
============================================================

Revenue: {money(revenue)}
Expenses: {money(expenses)}
Net Income: {money(net_income)}

Transactions Reviewed: {transactions_reviewed:,}
Unique Transactions Flagged: {unique_flagged:,}

High Priority: {high_count:,}
Medium Priority: {medium_count:,}
Low Priority: {low_count:,}

============================================================
BANK RECONCILIATION
============================================================

Matched Transactions: {matched_transactions:,}
Unmatched Transactions: {len(unmatched_items):,}
Reconciliation Rate: {reconciliation_rate:.2f}%

============================================================
INDEPENDENT GROUND-TRUTH VALIDATION
============================================================

Known Intentionally Embedded Anomalies: {known_anomalies:,}
Detected: {detected_anomalies:,}
Missed: {missed_anomalies:,}
Detection Rate: {detection_rate:.1f}%

VALIDATION LIMITATION

This validation result represents performance against
intentionally embedded anomalies in the project's synthetic
test environment.

The 100% detection result, where applicable, should not be
interpreted as universal real-world anomaly-detection accuracy.
Real company data may contain different transaction patterns,
data-quality issues, control environments, and anomaly types.

============================================================
AI-ASSISTED MANAGEMENT INTERPRETATION
============================================================

{ai_report_section}

============================================================
CONTROL NOTICE
============================================================

LedgerLens combines deterministic financial controls, anomaly
identification, risk prioritization, bank reconciliation,
independent synthetic validation, and generative AI to support
human financial review.

The generative AI layer interprets verified analytical results.
It does not independently perform the underlying financial
calculations or determine whether a transaction constitutes
fraud, misconduct, or an accounting error.

Flagged transactions require human verification and supporting
documentation before management reaches a final conclusion.
"""

    st.text_area(
        "Report Preview",
        report_text,
        height=560,
    )

    st.download_button(
        "⬇️ Download Management Report",
        data=report_text,
        file_name=(
            "LedgerLens_Management_Report.txt"
        ),
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# SYSTEM DESIGN
# ============================================================

elif page == "System Design":

    st.markdown(
        '<div class="section-title">'
        'LedgerLens System Design'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
LedgerLens is designed around a simple principle:
**financial conclusions should remain traceable to deterministic
analytics, while generative AI helps communicate those findings.**

### 1. Financial Data

Ledger transactions provide the base financial dataset.

↓

### 2. Deterministic Financial Controls

LedgerLens evaluates transaction characteristics including:

- possible duplicate transactions;
- unusually large amounts;
- material new vendors;
- category inconsistencies;
- round-dollar activity; and
- reconciliation exceptions.

↓

### 3. Risk Aggregation

Individual control signals are consolidated into
transaction-level risk scores and management-review priorities.

↓

### 4. Bank Reconciliation

Ledger records are compared against simulated banking activity
to identify matched and unmatched transactions.

↓

### 5. Independent Evaluation

Intentionally embedded ground-truth anomalies are used to test
whether the deterministic control framework successfully
identifies known test cases.

The current evaluation is a **synthetic benchmark**. Performance
against intentionally planted anomalies should not be interpreted
as universal real-world detection accuracy.

↓

### 6. Gemini Interpretation Layer

Verified LedgerLens results are supplied to Gemini to produce a
management-oriented financial and internal-control narrative.

Gemini interprets the analytical results. It does **not** replace
the underlying deterministic control framework.

↓

### 7. Human Review

Management reviews supporting documentation and determines
whether flagged activity represents:

- a legitimate transaction;
- a timing difference;
- a control issue;
- an accounting error;
- or another matter requiring follow-up.

The final conclusion remains a human decision.
"""
    )

    st.markdown(
        """
<div class="success-box">
<b>Design principle:</b>
LedgerLens is a decision-support system, not an autonomous fraud
determination system. The objective is to reduce the amount of
transaction-level noise a finance team must review manually and
direct attention toward exceptions that warrant investigation.
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    <b>LedgerLens AI • AI-Assisted Financial Review System</b>
    <br>
    Deterministic controls + risk prioritization + reconciliation
    + independent validation + generative AI interpretation
</div>
""",
    unsafe_allow_html=True,
)
