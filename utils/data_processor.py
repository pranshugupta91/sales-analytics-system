def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total = 0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total

def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }

    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    region_data = {}
    total_sales = calculate_total_revenue(transactions)

    for t in transactions:
        region = t["Region"]
        amount = t["Quantity"] * t["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_sales) * 100, 2
        )

    region_data = dict(
        sorted(region_data.items(),
               key=lambda x: x[1]["total_sales"],
               reverse=True)
    )

    return region_data

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples

    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]

    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "revenue": 0}

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    result = []
    for name in product_data:
        data = product_data[name]
        result.append((name, data["qty"], data["revenue"]))

    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics

    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }

    Requirements:
    - Calculate total amount spent per customer
    - Count number of purchases
    - Calculate average order value
    - List unique products bought
    - Sort by total_spent descending
    """
    customer_data = {}

    for t in transactions:
        cid = t["CustomerID"]
        amount = t["Quantity"] * t["UnitPrice"]
        product = t["ProductName"]

        if cid not in customer_data:
            customer_data[cid] = {
                "total_spent": 0,
                "purchase_count": 0,
                "products_bought": []
            }

        customer_data[cid]["total_spent"] += amount
        customer_data[cid]["purchase_count"] += 1

        if product not in customer_data[cid]["products_bought"]:
            customer_data[cid]["products_bought"].append(product)

    for cid in customer_data:
        total = customer_data[cid]["total_spent"]
        count = customer_data[cid]["purchase_count"]
        customer_data[cid]["avg_order_value"] = round(total / count, 2)

    customer_data = dict(
        sorted(customer_data.items(),
               key=lambda x: x[1]["total_spent"],
               reverse=True)
    )

    return customer_data

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date

    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }

    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """
    daily_data = {}

    for t in transactions:
        date = t["Date"]
        amount = t["Quantity"] * t["UnitPrice"]
        customer = t["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0,
                "transaction_count": 0,
                "customers": []
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1

        if customer not in daily_data[date]["customers"]:
            daily_data[date]["customers"].append(customer)

    result = {}
    for date in sorted(daily_data):
        result[date] = {
            "revenue": daily_data[date]["revenue"],
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)

    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """
    daily_data = daily_sales_trend(transactions)

    peak_date = ""
    max_revenue = 0
    count = 0

    for date in daily_data:
        if daily_data[date]["revenue"] > max_revenue:
            max_revenue = daily_data[date]["revenue"]
            peak_date = date
            count = daily_data[date]["transaction_count"]

    return peak_date, max_revenue, count


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples

    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]

    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """
    product_data = {}

    for t in transactions:
        name = t["ProductName"]
        qty = t["Quantity"]
        revenue = qty * t["UnitPrice"]

        if name not in product_data:
            product_data[name] = {"qty": 0, "revenue": 0}

        product_data[name]["qty"] += qty
        product_data[name]["revenue"] += revenue

    result = []
    for name in product_data:
        if product_data[name]["qty"] < threshold:
            result.append(
                (name, product_data[name]["qty"], product_data[name]["revenue"])
            )

    result.sort(key=lambda x: x[1])

    return result


