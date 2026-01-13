def read_sales_file(file_path):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()

            # Remove header and empty lines
            cleaned_lines = []
            for line in lines[1:]:   # skip header
                if line.strip():
                    cleaned_lines.append(line.strip())

            return cleaned_lines

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print("Error: File not found")
            return []

    print("Error: Unable to read file with supported encodings")
    return []


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]
    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip incorrect rows
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        # Clean product name
        pname = pname.replace(",", "")

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except:
            continue

        transaction = {
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        }

        transactions.append(transaction)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """

    valid_transactions = []
    invalid_count = 0

    summary = {
        "total_input": len(transactions),
        "invalid": 0,
        "filtered_by_region": 0,
        "filtered_by_amount": 0,
        "final_count": 0
    }

    # Display available regions
    regions = set(t["Region"] for t in transactions if t.get("Region"))
    print("Available regions:", regions)

    # Display transaction amount range
    amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
    print("Transaction amount range:", min(amounts), "-", max(amounts))

    for t in transactions:
        # Validation checks
        if (
            t["Quantity"] <= 0 or
            t["UnitPrice"] <= 0 or
            not t["TransactionID"].startswith("T") or
            not t["ProductID"].startswith("P") or
            not t["CustomerID"].startswith("C")
        ):
            invalid_count += 1
            continue

        amount = t["Quantity"] * t["UnitPrice"]

        # Region filter
        if region and t["Region"] != region:
            summary["filtered_by_region"] += 1
            continue

        # Amount filter
        if min_amount and amount < min_amount:
            summary["filtered_by_amount"] += 1
            continue

        if max_amount and amount > max_amount:
            summary["filtered_by_amount"] += 1
            continue

        valid_transactions.append(t)

    summary["invalid"] = invalid_count
    summary["final_count"] = len(valid_transactions)

    print("Records after validation:", summary["total_input"] - invalid_count)
    print("Records after filtering:", summary["final_count"])

    return valid_transactions, invalid_count, summary


raw_lines = read_sales_data("data/sales_data.txt")
transactions = parse_transactions(raw_lines)

valid_data, invalid_count, summary = validate_and_filter(
    transactions,
    region="North",
    min_amount=5000
)
