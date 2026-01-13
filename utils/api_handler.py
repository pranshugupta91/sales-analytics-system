import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        data = response.json()

        products = []

        for p in data["products"]:
            products.append({
                "id": p["id"],
                "title": p["title"],
                "category": p["category"],
                "brand": p["brand"],
                "price": p["price"],
                "rating": p["rating"]
            })

        print("API fetch successful. Products fetched:", len(products))
        return products

    except Exception as e:
        print("API fetch failed:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    mapping = {}

    for p in api_products:
        mapping[p["id"]] = {
            "title": p["title"],
            "category": p["category"],
            "brand": p["brand"],
            "rating": p["rating"]
        }

    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()
    Returns: list of enriched transaction dictionaries
    """
    enriched = []
    for t in transactions:
        product_id = t["ProductID"]

        try:
            numeric_id = int(product_id.replace("P", ""))
        except:
            numeric_id = None

        new_t = t.copy()

        if numeric_id in product_mapping:
            new_t["API_Category"] = product_mapping[numeric_id]["category"]
            new_t["API_Brand"] = product_mapping[numeric_id]["brand"]
            new_t["API_Rating"] = product_mapping[numeric_id]["rating"]
            new_t["API_Match"] = True
        else:
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    save_enriched_data(enriched)
    return enriched


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    """
    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(header) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID")),
                str(t.get("Date")),
                str(t.get("ProductID")),
                str(t.get("ProductName")),
                str(t.get("Quantity")),
                str(t.get("UnitPrice")),
                str(t.get("CustomerID")),
                str(t.get("Region")),
                str(t.get("API_Category")),
                str(t.get("API_Brand")),
                str(t.get("API_Rating")),
                str(t.get("API_Match"))
            ]

            file.write("|".join(row) + "\n")

    print("Enriched data saved to:", filename)

api_products = fetch_all_products()
product_mapping = create_product_mapping(api_products)
enriched_transactions = enrich_sales_data(transactions, product_mapping)

