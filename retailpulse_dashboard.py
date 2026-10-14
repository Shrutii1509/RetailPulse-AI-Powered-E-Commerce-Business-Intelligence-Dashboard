# retailpulse_dashboard.py
# Run: streamlit run retailpulse_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="RetailPulse — BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .kpi-box { background:#f0f6ff; border-left:4px solid #3b82f6;
               padding:16px 20px; border-radius:8px; margin-bottom:8px; }
    .kpi-label { font-size:13px; color:#57606a; font-weight:600; }
    .kpi-value { font-size:28px; font-weight:800; color:#1e3a5f; }
    .insight-box { background:#fffbeb; border-left:4px solid #f59e0b;
                   padding:14px 18px; border-radius:8px; margin:6px 0; }
    .section-header { font-size:20px; font-weight:700; color:#1e3a5f;
                      border-bottom:2px solid #e5e7eb; padding-bottom:6px; margin-top:16px; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data_cleaned.csv", parse_dates=["InvoiceDate"])
    except FileNotFoundError:
        df = pd.read_csv("../E-Commerce Data.csv/data.csv", encoding="unicode_escape")
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["InvoiceNo"] = df["InvoiceNo"].astype(str)
        df = df[~df["InvoiceNo"].str.startswith("C")]
        df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
        df = df.dropna(subset=["CustomerID", "Description"])
        df = df.drop_duplicates()
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    if "Revenue" not in df.columns:
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["Quarter"] = df["InvoiceDate"].dt.quarter
    df["Year"] = df["InvoiceDate"].dt.year
    return df

df = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/combo-chart.png", width=60)
st.sidebar.title("RetailPulse")
st.sidebar.markdown("*AI-Powered E-Commerce BI*")
st.sidebar.markdown("---")

all_countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect(
    "Filter by Country", all_countries, default=all_countries
)

date_min = df["InvoiceDate"].min().date()
date_max = df["InvoiceDate"].max().date()
date_range = st.sidebar.date_input(
    "Date Range", value=(date_min, date_max),
    min_value=date_min, max_value=date_max
)

# Apply filters
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    dff = df[
        (df["Country"].isin(selected_countries)) &
        (df["InvoiceDate"] >= start_date) &
        (df["InvoiceDate"] <= end_date)
    ]
else:
    dff = df[df["Country"].isin(selected_countries)]

st.sidebar.markdown(f"**Filtered rows:** {len(dff):,}")

# ── Header ────────────────────────────────────────────────────────────────
st.title("📊 RetailPulse: AI-Powered E-Commerce BI Dashboard")
st.markdown("*Online Retail Dataset (Dec 2010 – Dec 2011) · Author: Shrutisneha*")
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────
total_revenue = dff["Revenue"].sum()
total_orders = dff["InvoiceNo"].nunique()
unique_customers = dff["CustomerID"].nunique()
orders_per_cust = dff.groupby("CustomerID")["InvoiceNo"].nunique()
repeat_rate = (orders_per_cust >= 2).sum() / len(orders_per_cust) * 100
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class='kpi-box'>
      <div class='kpi-label'>💰 Total Revenue</div>
      <div class='kpi-value'>£{total_revenue:,.0f}</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class='kpi-box'>
      <div class='kpi-label'>🧾 Total Orders</div>
      <div class='kpi-value'>{total_orders:,}</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class='kpi-box'>
      <div class='kpi-label'>🔁 Repeat Customer Rate</div>
      <div class='kpi-value'>{repeat_rate:.1f}%</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class='kpi-box'>
      <div class='kpi-label'>🛒 Avg Order Value</div>
      <div class='kpi-value'>£{avg_order_value:,.2f}</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""
    <div class='kpi-box'>
      <div class='kpi-label'>👥 Unique Customers</div>
      <div class='kpi-value'>{unique_customers:,}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tab Layout ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sales Trends", "🏆 Top Products",
    "🌍 Country Analysis", "👥 Customer Behavior", "💡 Business Insights"
])

# ── Tab 1: Sales Trends ───────────────────────────────────────────────────
with tab1:
    st.markdown("<div class='section-header'>Monthly Revenue & Orders</div>", unsafe_allow_html=True)
    monthly = dff.groupby("YearMonth").agg(
        Revenue=("Revenue", "sum"),
        Orders=("InvoiceNo", "nunique")
    ).reset_index().sort_values("YearMonth")
    monthly["MoM_Growth"] = monthly["Revenue"].pct_change() * 100

    fig = make_subplots(rows=2, cols=1,
        subplot_titles=("Monthly Revenue (£)", "Monthly Orders"),
        shared_xaxes=True, vertical_spacing=0.12)
    fig.add_trace(go.Scatter(x=monthly["YearMonth"], y=monthly["Revenue"],
        fill="tozeroy", line=dict(color="#3b82f6", width=2.5), name="Revenue"), row=1, col=1)
    fig.add_trace(go.Bar(x=monthly["YearMonth"], y=monthly["Orders"],
        marker_color="#10b981", name="Orders"), row=2, col=1)
    fig.update_layout(template="plotly_white", height=520, showlegend=False)
    fig.update_yaxes(tickprefix="£", row=1, col=1)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.bar(monthly.dropna(subset=["MoM_Growth"]),
            x="YearMonth", y="MoM_Growth",
            title="Month-over-Month Growth (%)",
            color="MoM_Growth", color_continuous_scale="RdYlGn",
            text=monthly.dropna(subset=["MoM_Growth"])["MoM_Growth"].apply(lambda x: f"{x:.1f}%"))
        fig2.update_traces(textposition="outside")
        fig2.update_layout(template="plotly_white", height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow = dff.groupby("DayOfWeek")["InvoiceNo"].nunique().reindex(dow_order).reset_index()
        dow.columns = ["Day", "Orders"]
        fig3 = px.bar(dow, x="Day", y="Orders", title="Orders by Day of Week",
            color="Orders", color_continuous_scale="Blues", text="Orders")
        fig3.update_traces(textposition="outside")
        fig3.update_layout(template="plotly_white", height=380, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

# ── Tab 2: Top Products ───────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-header'>Top Products by Revenue & Quantity</div>", unsafe_allow_html=True)
    top_n = st.slider("Number of top products to show", 5, 25, 15)
    prod = dff.groupby(["StockCode","Description"]).agg(
        Revenue=("Revenue","sum"), Qty=("Quantity","sum"), Orders=("InvoiceNo","nunique")
    ).reset_index().sort_values("Revenue", ascending=False).head(top_n)

    c1, c2 = st.columns(2)
    with c1:
        fig4 = px.bar(prod.sort_values("Revenue"), x="Revenue", y="Description",
            orientation="h", title=f"Top {top_n} Products by Revenue",
            color="Revenue", color_continuous_scale="Blues")
        fig4.update_layout(template="plotly_white", height=500, showlegend=False)
        fig4.update_xaxes(tickprefix="£")
        st.plotly_chart(fig4, use_container_width=True)
    with c2:
        prod_qty = dff.groupby(["StockCode","Description"]).agg(
            Qty=("Quantity","sum")
        ).reset_index().sort_values("Qty", ascending=False).head(top_n)
        fig5 = px.bar(prod_qty.sort_values("Qty"), x="Qty", y="Description",
            orientation="h", title=f"Top {top_n} Products by Quantity",
            color="Qty", color_continuous_scale="Greens")
        fig5.update_layout(template="plotly_white", height=500, showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)

    # Pareto
    st.markdown("<div class='section-header'>Pareto — Revenue Concentration</div>", unsafe_allow_html=True)
    p_rev = dff.groupby("StockCode")["Revenue"].sum().sort_values(ascending=False).reset_index()
    p_rev["CumPct"] = p_rev["Revenue"].cumsum() / p_rev["Revenue"].sum() * 100
    p_rev["RankPct"] = (p_rev.index + 1) / len(p_rev) * 100
    fig6 = go.Figure(go.Scatter(x=p_rev["RankPct"], y=p_rev["CumPct"],
        fill="tozeroy", line=dict(color="#3b82f6", width=2)))
    fig6.add_vline(x=20, line_dash="dash", line_color="red", annotation_text="Top 20% SKUs")
    fig6.add_hline(y=80, line_dash="dash", line_color="orange", annotation_text="80% Revenue")
    fig6.update_layout(title="Pareto Chart — Product Revenue Concentration",
        xaxis_title="% of Products", yaxis_title="Cumulative Revenue %",
        template="plotly_white", height=380)
    st.plotly_chart(fig6, use_container_width=True)

# ── Tab 3: Country Analysis ───────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-header'>Country-wise Revenue Performance</div>", unsafe_allow_html=True)
    crev = dff.groupby("Country").agg(
        Revenue=("Revenue","sum"), Orders=("InvoiceNo","nunique"), Customers=("CustomerID","nunique")
    ).reset_index().sort_values("Revenue", ascending=False)
    crev["Revenue_Share"] = crev["Revenue"] / crev["Revenue"].sum() * 100

    fig7 = px.choropleth(crev, locations="Country", locationmode="country names",
        color="Revenue", hover_data=["Orders","Customers","Revenue_Share"],
        color_continuous_scale="Blues", title="Global Revenue Heatmap")
    fig7.update_layout(template="plotly_white", height=470)
    st.plotly_chart(fig7, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        non_uk = crev[crev["Country"] != "United Kingdom"].head(10)
        fig8 = px.bar(non_uk.sort_values("Revenue"), x="Revenue", y="Country",
            orientation="h", title="Top 10 International Markets (Excl. UK)",
            color="Revenue", color_continuous_scale="Blues")
        fig8.update_layout(template="plotly_white", height=420, showlegend=False)
        fig8.update_xaxes(tickprefix="£")
        st.plotly_chart(fig8, use_container_width=True)
    with c2:
        top8 = crev.head(8).copy()
        others = pd.DataFrame([{"Country":"Others","Revenue":crev.iloc[8:]["Revenue"].sum(),
            "Orders":0,"Customers":0,"Revenue_Share":0}])
        pie_d = pd.concat([top8, others], ignore_index=True)
        fig9 = px.pie(pie_d, names="Country", values="Revenue", title="Revenue Share by Country",
            color_discrete_sequence=px.colors.sequential.Blues_r)
        fig9.update_traces(textposition="inside", textinfo="percent+label")
        fig9.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig9, use_container_width=True)

    st.dataframe(crev[["Country","Revenue","Revenue_Share","Orders","Customers"]]
        .rename(columns={"Revenue_Share":"Share %"}).style.format(
        {"Revenue":"£{:,.2f}","Share %":"{:.1f}%","Orders":"{:,}","Customers":"{:,}"}),
        use_container_width=True)

# ── Tab 4: Customer Behavior ──────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-header'>RFM Customer Segmentation</div>", unsafe_allow_html=True)
    snap = dff["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = dff.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snap - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum")
    ).reset_index()
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
    rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    def seg(s):
        if s >= 10: return "Champions"
        elif s >= 8: return "Loyal Customers"
        elif s >= 6: return "Potential Loyalists"
        elif s >= 4: return "At Risk"
        else: return "Lost"
    rfm["Segment"] = rfm["RFM_Score"].apply(seg)

    c1, c2 = st.columns(2)
    with c1:
        seg_s = rfm["Segment"].value_counts().reset_index()
        seg_s.columns = ["Segment", "Customers"]
        fig10 = px.bar(seg_s, x="Segment", y="Customers", title="Customer Segments (RFM)",
            color="Segment", text="Customers",
            color_discrete_sequence=["#1e40af","#3b82f6","#60a5fa","#f59e0b","#ef4444"])
        fig10.update_traces(textposition="outside")
        fig10.update_layout(template="plotly_white", height=400, showlegend=False)
        st.plotly_chart(fig10, use_container_width=True)
    with c2:
        fig11 = px.scatter(rfm, x="Recency", y="Monetary", color="Segment",
            size="Frequency", hover_data=["CustomerID","Frequency"],
            title="RFM Scatter: Recency vs Monetary",
            color_discrete_sequence=["#1e40af","#3b82f6","#60a5fa","#f59e0b","#ef4444"])
        fig11.update_layout(template="plotly_white", height=400)
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown("<div class='section-header'>Hourly Buying Pattern</div>", unsafe_allow_html=True)
    hour_c = dff.groupby("Hour")["InvoiceNo"].nunique().reset_index()
    hour_c.columns = ["Hour", "Orders"]
    fig12 = px.line(hour_c, x="Hour", y="Orders", title="Orders by Hour of Day", markers=True)
    fig12.update_traces(line_color="#3b82f6", line_width=2.5)
    fig12.update_layout(template="plotly_white", height=370)
    st.plotly_chart(fig12, use_container_width=True)

# ── Tab 5: Business Insights ──────────────────────────────────────────────
with tab5:
    st.markdown("<div class='section-header'>AI-Assisted Business Insights</div>", unsafe_allow_html=True)

    uk_share = crev[crev["Country"]=="United Kingdom"]["Revenue_Share"].values
    uk_pct = uk_share[0] if len(uk_share) > 0 else 0
    one_time = (orders_per_cust == 1).sum()
    one_time_pct = one_time / unique_customers * 100

    st.markdown("### 📊 Key Facts")
    st.info(f"""
    - **Total Revenue:** £{total_revenue:,.2f} across **{total_orders:,}** orders
    - **Unique Customers:** {unique_customers:,} | **Avg Order Value:** £{avg_order_value:,.2f}
    - **Repeat Customer Rate:** {repeat_rate:.1f}% — indicating strong customer loyalty
    """)

    st.markdown("### 📈 Trends")
    monthly2 = dff.groupby("YearMonth").agg(Revenue=("Revenue","sum")).reset_index().sort_values("YearMonth")
    peak_m = monthly2.loc[monthly2["Revenue"].idxmax(), "YearMonth"]
    peak_r = monthly2["Revenue"].max()
    st.success(f"""
    - **Peak Month:** {peak_m} with £{peak_r:,.0f} in revenue
    - **Q4 (Oct–Dec)** consistently outperforms all other quarters — holiday season effect
    - **Peak buying hours:** 10 AM – 3 PM on weekdays (especially Thursday)
    """)

    st.markdown("### ⚠️ Risks")
    st.warning(f"""
    - **Geographic concentration:** UK accounts for {uk_pct:.1f}% of revenue — over-reliance on single market
    - **{one_time_pct:.1f}% one-time buyers** ({one_time:,} customers) — high churn if not re-engaged
    - **Heavy SKU dependency:** Top 20% of products drive ~80% of revenue
    """)

    st.markdown("### 🚀 Opportunities")
    top2_c = crev.iloc[1]["Country"] if len(crev) > 1 else "N/A"
    top2_s = crev.iloc[1]["Revenue_Share"] if len(crev) > 1 else 0
    st.success(f"""
    - **International expansion:** {top2_c} is the #2 market ({top2_s:.1f}% share) — strong growth potential
    - **Loyalty program:** {repeat_rate:.1f}% repeat rate signals receptive base for VIP tiers
    - **Bundle & upsell:** High-frequency SKUs offer cross-sell opportunities
    """)

    st.markdown("### ✅ Actionable Recommendations")
    st.markdown("""
    1. 🎯 **Win-back campaign** for "At Risk" RFM customers — personalized email with discount codes
    2. 📧 **Post-purchase sequences** to convert one-time buyers into repeat customers
    3. 👑 **VIP loyalty tier** for Champions — exclusive early access and rewards
    4. 🌍 **EU market investment** — Netherlands, Germany, France show strong demand signals
    5. 📦 **Q4 inventory planning** — stock top SKUs by September to capture holiday surge
    6. 🔥 **January flash sale** — counter post-holiday revenue dip with limited-time offers
    7. ⏰ **Optimize ad spend** for 10 AM–12 PM window — highest order conversion rate
    """)

# ── Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center; color:#57606a; font-size:13px;'>RetailPulse · AI-Powered E-Commerce BI Dashboard · Shrutisneha · 2024</p>",
    unsafe_allow_html=True)