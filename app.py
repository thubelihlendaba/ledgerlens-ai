import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime
import html

# ============================================================
# LEDGERLENS AI
# Streamlit Management Review Application
# ============================================================

st.set_page_config(
    page_title="LedgerLens AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background-color: #0b2942;
        }

        [data-testid="stSidebar"] * {
            color: white;
        }

        .main-header {
            background: linear-gradient(135deg, #123b5d, #245f86);
            padding: 32px 36px;
            border-radius: 16px;
            margin-bottom: 22px;
            color: white;
        }

        .main-header h1 {
            margin: 0;
            font-size: 42px;
            font-weight: 750;
        }

        .main-header p {
            margin-top: 8px;
            margin-bottom: 0;
            font-size: 16px;
            opacity: 0.92;
        }

        .section-title {
            font-size: 23px;
            font-weight: 700;
            color: #123b5d;
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .info-box {
            padding: 18px;
            border-radius: 12px;
            background-color: #eef5fa;
            border-left: 5px solid #2b6f9f;
            margin-bottom: 18px;
        }

        .risk-high {
            color: #b42318;
            font-weight: 700;
        }

        .risk-medium {
            color: #b54708;
            font-weight: 700;
        }

        .risk-low {
            color: #175cd3;
            font-weight: 700;
        }

        .footer {
            text-align: center;
            color: #667085;
            font-size: 12px;
            padding-top: 35px;
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
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"


def numeric_series(df, column):
    if column is None or df.empty:
        return pd.Series(dtype=float)

    return pd.to_numeric(df[column], errors="coerce").fillna(0)


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
# CALCULATE FINANCIAL METRICS
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
    revenue = numeric_series(monthly_summary, rev_col).sum()

if exp_col:
    expenses = numeric_series(monthly_summary, exp_col).sum()

if net_col:
    net_income = numeric_series(monthly_summary, net_col).sum()
else:
    net_income = revenue - expenses


# Fallback calculation using transaction-level data
if revenue == 0 and not clean_transactions.empty:

    amount_col = find_column(
        clean_transactions,
        ["Amount"]
    )

    type_col = find_column(
        clean_transactions,
        ["Transaction_Type", "Transaction Type", "Type"]
    )

    if amount_col and type_col:

        types = clean_transactions[type_col].astype(str).str.lower()

        revenue = pd.to_numeric(
            clean_transactions.loc[
                types.str.contains("revenue|income", regex=True),
                amount_col
            ],
            errors="coerce"
        ).sum()

        expenses = pd.to_numeric(
            clean_transactions.loc[
                types.str.contains("expense", regex=True),
                amount_col
            ],
            errors="coerce"
        ).sum()

        net_income = revenue - expenses


# ============================================================
# CONTROL / RISK METRICS
# ============================================================

transactions_reviewed = len(clean_transactions)

if transactions_reviewed == 0:
    transactions_reviewed = len(transactions)

unique_flagged = len(transaction_risk)

priority_col = find_column(
    transaction_risk,
    ["Priority", "Risk_Level", "Risk Level"]
)

if priority_col:

    priority_values = (
        transaction_risk[priority_col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    high_count = int((priority_values == "high").sum())
    medium_count = int((priority_values == "medium").sum())
    low_count = int((priority_values == "low").sum())

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
        matched_transactions / transactions_reviewed
    ) * 100

else:

    reconciliation_rate = 0


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
    ["Evaluation_Result", "Result"]
)

if detected_col:

    detected_anomalies = (
        evaluation_results[detected_col]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes", "detected"])
        .sum()
    )

elif result_col:

    detected_anomalies = (
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
        detected_anomalies / known_anomalies
    ) * 100

else:

    detection_rate = 0


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
    """
    <div class="main-header">
        <div style="font-size:13px;letter-spacing:3px;font-weight:700;">
            AI-ASSISTED FINANCIAL REVIEW
        </div>

        <h1>LedgerLens AI</h1>

        <p>
            Financial controls • anomaly detection • reconciliation •
            risk prioritization • AI-assisted management interpretation
        </p>
    </div>
    """,
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

    fig.update_layout(
        xaxis_title="Risk Priority",
        yaxis_title="Transactions",
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Flagged transactions represent items requiring human "
        "verification. A LedgerLens alert does not independently "
        "establish fraud, misconduct, or accounting error."
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

        st.dataframe(
            monthly_summary,
            use_container_width=True,
            hide_index=True,
        )

        month_col = find_column(
            monthly_summary,
            ["Month", "Date", "Period"]
        )

        chart_columns = [
            col
            for col in [rev_col, exp_col, net_col]
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

            fig = px.line(
                chart_df,
                x=month_col,
                y="Amount",
                color="Financial Metric",
                markers=True,
                title="Monthly Financial Performance",
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

    c1.metric("High Priority", high_count)
    c2.metric("Medium Priority", medium_count)
    c3.metric("Low Priority", low_count)
    c4.metric("Total Flagged", unique_flagged)

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

        st.dataframe(
            risk_display,
            use_container_width=True,
            hide_index=True,
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
                "Search transaction ID, vendor, category, "
                "description, amount..."
            ),
        )

        filtered = source_df.copy()

        if search:

            mask = filtered.astype(str).apply(
                lambda column:
                column.str.contains(
                    search,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            filtered = filtered[mask]

        st.caption(
            f"{len(filtered):,} transactions displayed"
        )

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True,
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
            max(reconciliation_rate / 100, 0),
            1
        )
    )

    st.markdown("### Unmatched Items")

    if unmatched_items.empty:

        st.success(
            "No unmatched transactions were identified."
        )

    else:

        st.dataframe(
            unmatched_items,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "Unmatched items require follow-up against subsequent "
            "bank activity or supporting documentation. Timing "
            "differences may explain legitimate unmatched entries."
        )


# ============================================================
# MODEL EVALUATION
# ============================================================

elif page == "Model Evaluation":

    st.markdown(
        '<div class="section-title">Independent Ground-Truth Validation</div>',
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
        <b>Validation methodology:</b>
        The ground-truth dataset contains intentionally embedded
        anomalies used to evaluate LedgerLens after deterministic
        financial-control and risk-scoring processes have been
        applied. This is a synthetic benchmark and should not be
        interpreted as universal real-world anomaly-detection
        accuracy.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not evaluation_results.empty:

        st.markdown("### Transaction-Level Evaluation")

        st.dataframe(
            evaluation_results,
            use_container_width=True,
            hide_index=True,
        )

    if not evaluation_summary.empty:

        st.markdown("### Evaluation Summary")

        st.dataframe(
            evaluation_summary,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# AI MANAGEMENT REVIEW
# ============================================================

elif page == "AI Management Review":

    st.markdown(
        '<div class="section-title">Gemini-Assisted Management Review</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        LedgerLens performs deterministic financial controls,
        reconciliation, anomaly identification, and risk
        prioritization first.

        Gemini is then used as an **interpretation layer** to convert
        verified analytical results into a management-oriented review.
        The generative AI layer does not independently label a
        transaction as fraud or accounting error.
        """
    )

    st.markdown("### Verified Analytical Context")

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

    if "ai_review" not in st.session_state:
        st.session_state.ai_review = ""

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
                    "Gemini API key has not yet been configured "
                    "in Streamlit Secrets."
                )

            else:

                client = genai.Client(
                    api_key=api_key
                )

                risk_context = ""

                if not transaction_risk.empty:

                    risk_context = (
                        transaction_risk
                        .head(25)
                        .to_string(index=False)
                    )

                unmatched_context = ""

                if not unmatched_items.empty:

                    unmatched_context = (
                        unmatched_items
                        .head(10)
                        .to_string(index=False)
                    )

                prompt = f"""
You are assisting with a management-level financial review.

The analytical calculations below were already produced by
LedgerLens using deterministic financial controls. Do not invent
transactions, amounts, control failures, or allegations.

Company:
Lakeview Consulting LLC

Reporting period:
January through June 2026

Verified financial metrics:
Revenue: {money(revenue)}
Expenses: {money(expenses)}
Net income: {money(net_income)}

Control review:
Transactions reviewed: {transactions_reviewed}
Unique flagged transactions: {unique_flagged}
High priority: {high_count}
Medium priority: {medium_count}
Low priority: {low_count}

Bank reconciliation:
Matched transactions: {matched_transactions}
Unmatched transactions: {len(unmatched_items)}
Reconciliation rate: {reconciliation_rate:.2f}%

Synthetic ground-truth evaluation:
Known anomalies: {known_anomalies}
Detected anomalies: {detected_anomalies}
Missed anomalies: {missed_anomalies}
Detection rate: {detection_rate:.1f}%

Transaction risk data:
{risk_context}

Unmatched items:
{unmatched_context}

Prepare a professional management review with these sections:

1. Executive Summary
2. Financial Performance
3. Key Review Findings
4. Reconciliation and Controls
5. Recommended Management Actions
6. Conclusion

Use professional financial-review language.

Clearly distinguish an anomaly or review flag from confirmed fraud,
misconduct, or accounting error.

Do not claim that generative AI performed the underlying financial
controls. LedgerLens performed the analytical controls and Gemini is
providing management-oriented interpretation of those results.
"""

                with st.spinner(
                    "Gemini is preparing the management review..."
                ):

                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )

                st.session_state.ai_review = (
                    response.text
                    if response.text
                    else "No review was returned."
                )

        except Exception as error:

            st.error(
                f"AI review could not be generated: {error}"
            )

    if st.session_state.ai_review:

        st.markdown("---")

        st.markdown(
            st.session_state.ai_review
        )

        st.download_button(
            "⬇️ Download AI Management Review",
            data=st.session_state.ai_review,
            file_name="LedgerLens_AI_Management_Review.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# MANAGEMENT REPORT
# ============================================================

elif page == "Management Report":

    st.markdown(
        '<div class="section-title">Management Report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        This section consolidates LedgerLens financial results,
        control findings, reconciliation results, independent
        validation, and AI-assisted interpretation into a
        management-ready summary.
        """
    )

    report_text = f"""
LEDGERLENS AI
MANAGEMENT REVIEW REPORT

Lakeview Consulting LLC
January - June 2026

Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

============================================================
EXECUTIVE FINANCIAL SUMMARY
============================================================

Revenue: {money(revenue)}
Expenses: {money(expenses)}
Net Income: {money(net_income)}

Transactions Reviewed: {transactions_reviewed}
Unique Transactions Flagged: {unique_flagged}

High Priority: {high_count}
Medium Priority: {medium_count}
Low Priority: {low_count}

============================================================
BANK RECONCILIATION
============================================================

Matched Transactions: {matched_transactions}
Unmatched Transactions: {len(unmatched_items)}
Reconciliation Rate: {reconciliation_rate:.2f}%

============================================================
INDEPENDENT GROUND-TRUTH VALIDATION
============================================================

Known Anomalies: {known_anomalies}
Detected: {detected_anomalies}
Missed: {missed_anomalies}
Detection Rate: {detection_rate:.1f}%

This validation result represents performance against intentionally
embedded anomalies in the project's synthetic test environment.
It should not be interpreted as universal real-world detection
accuracy.

============================================================
AI-ASSISTED MANAGEMENT INTERPRETATION
============================================================

{st.session_state.get("ai_review", "AI management review has not yet been generated.")}

============================================================
CONTROL NOTICE
============================================================

LedgerLens combines deterministic financial controls, anomaly
detection, risk prioritization, reconciliation, independent
validation, and generative AI to support human financial review.

Flagged transactions require human verification and do not
independently establish fraud, misconduct, or accounting error.
"""

    st.text_area(
        "Report Preview",
        report_text,
        height=500,
    )

    st.download_button(
        "⬇️ Download Management Report",
        data=report_text,
        file_name="LedgerLens_Management_Report.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# SYSTEM DESIGN
# ============================================================

elif page == "System Design":

    st.markdown(
        '<div class="section-title">LedgerLens System Design</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
### 1. Financial Data

Ledger transactions provide the base financial dataset.

↓

### 2. Deterministic Financial Controls

LedgerLens evaluates transaction characteristics including
duplicates, unusual amounts, new vendors, categorization,
round-dollar activity, and reconciliation exceptions.

↓

### 3. Risk Aggregation

Individual control signals are consolidated into
transaction-level risk scores and management priorities.

↓

### 4. Bank Reconciliation

Ledger records are compared against banking activity to identify
matched and unmatched transactions.

↓

### 5. Independent Evaluation

Intentionally embedded ground-truth anomalies are used to test
whether the control framework successfully identifies known test
cases.

↓

### 6. Gemini Interpretation Layer

Verified LedgerLens results are supplied to Gemini to produce a
management-oriented narrative.

Gemini interprets the analytical results. It does **not** replace
the underlying deterministic control framework.

↓

### 7. Human Review

Management evaluates supporting documentation and determines
whether flagged activity represents a legitimate transaction,
control issue, accounting error, or another matter requiring
follow-up.
"""
    )

    st.success(
        "LedgerLens is designed as a decision-support system, "
        "not an autonomous fraud determination system."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        LedgerLens AI • AI-Assisted Financial Review System<br>
        Deterministic controls + risk prioritization +
        reconciliation + independent validation +
        generative AI interpretation
    </div>
    """,
    unsafe_allow_html=True,
)
