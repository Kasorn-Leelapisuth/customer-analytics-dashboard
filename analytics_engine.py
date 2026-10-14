# Import sqlite3 to run SQL queries locally
import sqlite3
# Import os to check if files exist
import os
# Import pandas to run SQL queries directly into dataframes
import pandas as pd

DB_NAME = "ecommerce.db"
CSV_FILE = "ecommerce_orders.csv"


def load_csv_to_db():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_NAME)

    # Read CSV into pandas DataFrame
    df = pd.read_csv(CSV_FILE)

    # Write data into a table named 'orders' (replace if exists)
    df.to_sql("orders", conn, if_exists="replace", index=False)

    conn.close()
    print("CSV loaded into SQLite database successfully.")


def get_summary_kpis():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_NAME)

    # SQL Query 1: Calculate total completed revenue, total orders, and average order value (AOV)
    query = """
        SELECT
            COUNT(order_id) AS total_orders,
            SUM(CASE WHEN status = 'Completed' THEN total_spend ELSE 0 END) AS total_revenue,
            AVG(CASE WHEN status = 'Completed' THEN total_spend ELSE NULL END) AS average_order_value,
            COUNT(DISTINCT customer_id) AS total_unique_customers
        FROM orders;
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


def get_monthly_revenue():
    conn = sqlite3.connect(DB_NAME)

    # SQL Query 2: Group revenue by Year-Month
    query = """
        SELECT 
            strftime('%Y-%m', order_date) AS order_month,
            SUM(total_spend) AS monthly_revenue,
            COUNT(order_id) AS orders_count
        FROM orders
        WHERE status = 'Completed'
        GROUP BY order_month
        ORDER BY order_month ASC;
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


def get_top_products_by_revenue():
    conn = sqlite3.connect(DB_NAME)

    # SQL Query 3: Using Window Function (RANK) to find top performing products
    query = """
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
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


def get_repeat_customer_rate():
    conn = sqlite3.connect(DB_NAME)

    # SQL Query 4: CTE to calculate how many customers made more than 1 purchase
    query = """
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
    """
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


if __name__ == "__main__":
    load_csv_to_db()