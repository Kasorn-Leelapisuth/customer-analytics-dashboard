# Executive E-Commerce & Customer Retention Analytics Dashboard

An end-to-end data analytics and business intelligence platform built using Python, SQLite, SQL Window Functions, and Streamlit. This tool processes raw transaction logs, models key retail performance metrics, and translates relational data into executive-level retention and product revenue insights.

---
##  Business Problem & Impact

Retail businesses require clear visibility into repeat purchase behavior, product revenue distributions, and month-over-month sales velocity. This dashboard addresses these questions through:
- **Executive KPIs:** Live metrics tracking Total Completed Revenue, Total Volume, Average Order Value (AOV), and Repeat Customer Rate.
- **SQL Window Function Ranking:** Utilizes Common Table Expressions (CTEs) and `RANK() OVER (ORDER BY revenue DESC)` to rank best-selling product categories dynamically.
- **Sales Velocity Visualizations:** Interactive Plotly charts evaluating monthly revenue trends and category performance.

---

## Tech Stack

- **Data Processing:** Python, pandas
- **Database & Query Engine:** SQLite (CTEs, Aggregate Functions, Window Functions)
- **Data Visualization:** Plotly Express
- **Dashboard Framework:** Streamlit

---

## Key SQL Queries Implemented

### 1. Repeat Customer Rate (Cohort Analysis via CTE)
```sql
WITH CustomerOrderCounts AS (
    SELECT 
        customer_id, 
        COUNT(order_id) AS orders_placed
    FROM orders
    WHERE status = 'Completed'
    GROUP BY customer_id
)
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN orders_placed > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND((CAST(SUM(CASE WHEN orders_placed > 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100, 2) AS repeat_rate_pct
FROM CustomerOrderCounts;

---
### 2. Product Revenue Ranking (Window Function) 
 ```sql
 WITH ProductSales AS (
    SELECT 
        category,
        product_name,
        SUM(total_spend) AS product_revenue,
        SUM(quantity) AS units_sold
    FROM orders
    WHERE status = 'Completed'
    GROUP BY category, product_name
)
SELECT 
    category,
    product_name,
    product_revenue,
    units_sold,
    RANK() OVER (ORDER BY product_revenue DESC) AS sales_rank
FROM ProductSales;
```