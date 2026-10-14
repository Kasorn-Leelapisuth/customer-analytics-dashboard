# Import csv to write data directly into a CSV file
import csv
# Import datetime to generate realistic order dates across several months
from datetime import datetime, timedelta
# Import random to generate random order values and customer choices
import random

# Output file name
CSV_FILE = "ecommerce_orders.csv"

# List of realistic product categories and sample items
PRODUCTS = {
    "Electronics": [
        ("Mechanical Keyboard", 120.0),
        ("Wireless Mouse", 45.0),
        ("USB-C Hub", 35.0),
    ],
    "Office Supplies": [
        ("Ergonomic Chair Pad", 50.0),
        ("Desk Mat", 25.0),
        ("LED Monitor Light", 60.0),
    ],
    "Accessories": [
        ("Laptop Stand", 40.0),
        ("Cable Management Kit", 15.0),
        ("Screen Cleaning Kit", 12.0),
    ],
}

# Status choices for orders
STATUS_CHOICES = ["Completed", "Completed", "Completed", "Refunded"]


def generate_records(num_rows=250):
    start_date = datetime(2026, 1, 1)

    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "order_id",
            "customer_id",
            "category",
            "product_name",
            "unit_price",
            "quantity",
            "total_spend",
            "status",
            "order_date",
        ])

        for order_id in range(1001, 1001 + num_rows):
            customer_id = f"CUST-{random.randint(101, 160)}"
            category = random.choice(list(PRODUCTS.keys()))
            product_name, unit_price = random.choice(PRODUCTS[category])
            quantity = random.randint(1, 3)
            total_spend = round(unit_price * quantity, 2)
            status = random.choice(STATUS_CHOICES)
            days_offset = random.randint(0, 180)
            order_date = (start_date + timedelta(days=days_offset)).strftime(
                "%Y-%m-%d"
            )

            writer.writerow([
                order_id,
                customer_id,
                category,
                product_name,
                unit_price,
                quantity,
                total_spend,
                status,
                order_date,
            ])

    print(f"Generated {num_rows} transactions in '{CSV_FILE}'.")


if __name__ == "__main__":
    generate_records(250)