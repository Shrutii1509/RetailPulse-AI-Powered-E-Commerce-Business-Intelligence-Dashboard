# 📊 RetailPulse: AI-Powered E-Commerce Business Intelligence Dashboard

**Author:** Shrutisneha  
**Project Type:** Data Analysis & Business Intelligence  
**Technologies:** Python · Pandas · Plotly · Streamlit  

---

## 🗂️ Project Overview

RetailPulse is a full-stack business intelligence dashboard built on a real-world e-commerce transaction dataset. It performs end-to-end data analysis — from raw data ingestion and cleaning through exploratory analysis, KPI computation, customer segmentation, and interactive visualization — and presents actionable AI-assisted business insights via an interactive Streamlit web application.

The project answers critical business questions:
- How is revenue trending over time, and when does demand peak?
- Which products and markets drive the most value?
- Which customers are loyal, at risk, or churning?
- What concrete actions should the business take to grow?

---

## 📁 Project Structure

```
RetailPulse/
├── Shrutisneha_RetailPulse.ipynb   ← Main code submission (Jupyter Notebook)
├── retailpulse_dashboard.py        ← Standalone Streamlit dashboard
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
├── Shrutisneha_ProjectReport.docx  ← Full project report (Word)
└── data_cleaned.csv                ← Generated after running the notebook
```

> **Note:** The raw dataset (`data.csv`) lives in `../E-Commerce Data.csv/data.csv` relative to the project folder. The notebook loads it from there and saves the cleaned version as `data_cleaned.csv` in the project folder.

---

## 📦 Dataset Information

| Property | Value |
|---|---|
| **File** | `E-Commerce Data.csv/data.csv` |
| **Source** | Online Retail Dataset (UCI Machine Learning Repository) |
| **Period** | December 2010 – December 2011 |
| **Raw Rows** | ~541,909 transaction lines |
| **Columns** | InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country |
| **Scope** | UK-based online retailer selling gift and home décor items |

### Column Descriptions

| Column | Type | Description |
|---|---|---|
| `InvoiceNo` | String | Unique invoice number; prefix `C` = cancellation |
| `StockCode` | String | Unique product/SKU code |
| `Description` | String | Product name |
| `Quantity` | Integer | Units ordered (negative = return/cancellation) |
| `InvoiceDate` | DateTime | Date and time of transaction |
| `UnitPrice` | Float | Price per unit in GBP (£) |
| `CustomerID` | Float | Unique customer identifier (nullable) |
| `Country` | String | Customer country |

---

## 🔬 Data Cleaning Summary

| Issue | Action |
|---|---|
| Duplicate rows | Removed |
| Cancelled invoices (`C` prefix) | Removed |
| Negative / zero quantities | Removed |
| Zero / negative unit prices | Removed |
| Missing `CustomerID` | Removed |
| Invalid / blank descriptions | Removed |
| Incorrect data types | Fixed (datetime, nullable int, string) |
| Feature engineering | Added `Revenue`, `YearMonth`, `DayOfWeek`, `Hour`, `Quarter` |

---

## 📊 Key Analyses

### 1. KPI Dashboard
- **Total Revenue** — sum of `Quantity × UnitPrice` for all cleaned transactions
- **Total Orders** — count of unique invoice numbers
- **Repeat Customer Rate** — % of customers who placed ≥ 2 distinct orders

### 2. Sales Trends
- Monthly revenue and order trends (Dec 2010 – Dec 2011)
- Month-over-month growth rates
- Quarterly breakdowns
- Day-of-week and hour-of-day order patterns

### 3. Top Products
- Top 15 SKUs by revenue and by quantity
- Pareto analysis (80/20 rule on product revenue concentration)

### 4. Country Analysis
- Revenue by country — choropleth world map
- Top 10 international markets (ex-UK)
- Revenue share pie chart

### 5. Customer Behavior (RFM)
- **Recency** — days since last purchase
- **Frequency** — number of unique orders
- **Monetary** — total spend
- **Segments:** Champions, Loyal Customers, Potential Loyalists, At Risk, Lost

### 6. AI-Assisted Business Insights
Facts, trends, risks, opportunities, and 7 actionable recommendations — all derived from actual data.

---

## 🛠️ Technologies Used

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Core language |
| Pandas | ≥ 1.5 | Data manipulation & cleaning |
| NumPy | ≥ 1.23 | Numerical operations |
| Plotly | ≥ 5.13 | Interactive visualizations |
| Streamlit | ≥ 1.22 | Web dashboard framework |
| Jupyter Notebook | ≥ 6.5 | Code submission format |

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Step 1 — Clone or place the project

Ensure the project folder and dataset are in the same parent directory:

```
Documents/
├── BOB2/
│   └── E-Commerce Data.csv/
│       └── data.csv
│   └── RetailPulse/
│       ├── Shrutisneha_RetailPulse.ipynb
│       ├── retailpulse_dashboard.py
│       ├── requirements.txt
│       └── README.md
```

### Step 2 — Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Steps to Run the Project

### Option A — Jupyter Notebook (main code submission)

```bash
cd RetailPulse
jupyter notebook Shrutisneha_RetailPulse.ipynb
```

Run all cells top-to-bottom. The notebook will:
1. Load and inspect the raw CSV
2. Clean the data and save `data_cleaned.csv`
3. Perform EDA and generate all plots
4. Calculate KPIs
5. Run RFM segmentation
6. Print AI-assisted business insights
7. Write `retailpulse_dashboard.py` to disk

### Option B — Streamlit Dashboard

After running the notebook at least once (to generate `data_cleaned.csv`):

```bash
cd RetailPulse
streamlit run retailpulse_dashboard.py
```

Then open your browser at **http://localhost:8501**

The dashboard provides:
- Sidebar filters (country, date range)
- 5 interactive tabs: Sales Trends, Top Products, Country Analysis, Customer Behavior, Business Insights
- Live KPI cards at the top
- All Plotly charts are fully interactive (hover, zoom, filter)

---

## 🗝️ Key Findings (Summary)

> All figures are computed from actual cleaned data.

- The business processed **hundreds of thousands** of transactions from customers across **37+ countries**
- **United Kingdom dominates** revenue (>80% share) — geographic diversification is a strategic priority
- **Q4 (Oct–Dec) is peak season** — November and December are consistently the top months
- **Repeat Customer Rate exceeds 90%** — the loyal customer base is a key competitive asset
- **Top 20% of SKUs contribute ~80% of revenue** — classic Pareto concentration
- **RFM segmentation** identifies actionable cohorts: Champions, At Risk, and Lost customers each require distinct engagement strategies

---

## 📄 Submission Files

| File | Description |
|---|---|
| `Shrutisneha_RetailPulse.ipynb` | Complete Jupyter Notebook (main code submission) |
| `retailpulse_dashboard.py` | Standalone Streamlit dashboard |
| `requirements.txt` | Python library dependencies |
| `README.md` | Project overview and setup guide |
| `Shrutisneha_ProjectReport.docx` | Full project report with analysis and screenshots |

---

## 📌 Notes

- The original `data.csv` is **never modified** — only read
- Cleaned data is saved separately as `data_cleaned.csv`
- All visualizations use Plotly for interactivity (hover, zoom, filter)
- The dashboard auto-recalculates all metrics when sidebar filters change
- No values are invented — every number in the insights section is computed from the actual dataset

---

*RetailPulse · AI-Powered E-Commerce BI Dashboard · Shrutisneha · 2024*
