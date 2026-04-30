# Business_Analytics

# End-to-End Business Intelligence & Analytics Portfolio

This integrated Python project demonstrates a complete **Business Intelligence** pipeline, performing **Customer Analytics** and **Financial Analytics** to derive actionable insights.

## Project Overview

The project includes:
1. **Customer & Marketing Analytics:** Retail dataset analysis with RFM, sales trends, and category performance.
2. **Financial Analytics & Market Research:** AAPL stock data analysis, financial metrics, and trend analysis.
3. **Data Visualization:** Interactive visualizations using the generated analytics outputs.

## Skills & Technologies Demonstrated

* **Programming:** Python (Pandas, NumPy, Plotly, yfinance)
* **Data Analysis:** Customer Analytics, Marketing Analytics, Financial Analytics, Trend Analysis
* **Reporting:** Excel output generation with `openpyxl`
* **Visualization:** Plotly visualizations and HTML dashboard export

## Repository Structure

```
Business-Analytics-Portfolio/
├── Analytics/
│   ├── 1_Customer_Analytics.ipynb
│   └── 2_Financial_Analytics.ipynb
├── visualization/
│   └── 3_Data_Visualization.ipynb
├── data/
│   └── SampleSuperstore.csv
├── dashboard/
│   ├── customer_dashboard.html
│   ├── financial_dashboard.html
│   ├── DAX_measures.txt
│   ├── PowerQuery_M.txt
│   ├── SampleSuperstore.csv
│   └── Tableau_Calculated_Fields.txt
├── report/
│   ├── customer_analytics_report.xlsx
│   └── financial_analysis_report.xlsx
├── generate_data.py
├── requirements.txt
└── README.md
```

## Notes

* `3_Data_Visualization.ipynb` was empty and has been populated with working dashboard visualizations.
* The project uses locally generated analytics output files in `report/`.
* The `dashboard/` folder contains HTML dashboard exports and BI notes.

## How to Run

1. Open `Analytics/1_Customer_Analytics.ipynb` and run the notebook.
2. Open `Analytics/2_Financial_Analytics.ipynb` and run the notebook.
3. Open `visualization/3_Data_Visualization.ipynb` and run to view interactive visualizations.

## Requirements

Install dependencies with:
```
pip install -r requirements.txt
```
