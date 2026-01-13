from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    Report Must Include (in this order):
    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed
    2. OVERALL SUMMARY
       - Total Revenue (formatted with commas)
       - Total Transactions
       - Average Order Value
       - Date Range of data
    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total Sales Amount
         * Percentage of Total
         * Transaction Count
       - Sorted by sales amount descending
    4. TOP 5 PRODUCTS
       - Table with columns: Rank, Product Name, Quantity Sold, Revenue
    5. TOP 5 CUSTOMERS
       - Table with columns: Rank, Customer ID, Total Spent, Order Count
    6. DAILY SALES TREND
       - Table showing: Date, Revenue, Transactions, Unique Customers
    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region
    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched
    """
    with open(output_file, "w", encoding="utf-8") as file:

        # 1. HEADER
        file.write("=" * 50 + "\n")
        file.write("        SALES ANALYTICS REPORT\n")
        file.write(f"      Generated: {datetime.now()}\n")
        file.write(f"      Records Processed: {len(transactions)}\n")
        file.write("=" * 50 + "\n\n")

        # 2. OVERALL SUMMARY
        total_revenue = calculate_total_revenue(transactions)
        avg_order = total_revenue / len(transactions)
        dates = [t["Date"] for t in transactions]
        file.write("OVERALL SUMMARY\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions:   {len(transactions)}\n")
        file.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        file.write(f"Date Range:           {min(dates)} to {max(dates)}\n\n")

        # 3. REGION-WISE PERFORMANCE
        region_data = region_wise_sales(transactions)
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 50 + "\n")
        file.write("Region    Sales        % of Total  Transactions\n")

        for region, data in region_data.items():
            file.write(
                f"{region:<10} ₹{data['total_sales']:,.2f}   "
                f"{data['percentage']:>6}%      {data['transaction_count']}\n"
            )
        file.write("\n")

        # 4. TOP 5 PRODUCTS
        top_products = top_selling_products(transactions, 5)
        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 50 + "\n")
        file.write("Rank  Product Name        Quantity  Revenue\n")
        rank = 1
        for p in top_products:
            file.write(
                f"{rank:<5} {p[0]:<18} {p[1]:<8} ₹{p[2]:,.2f}\n"
            )
            rank += 1
        file.write("\n")

        # 5. TOP 5 CUSTOMERS
        customers = customer_analysis(transactions)
        top_customers = list(customers.items())[:5]
        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 50 + "\n")
        file.write("Rank  Customer  Total Spent  Orders\n")
        rank = 1
        for cid, data in top_customers:
            file.write(
                f"{rank:<5} {cid:<9} ₹{data['total_spent']:,.2f}  "
                f"{data['purchase_count']}\n"
            )
            rank += 1
        file.write("\n")

        # 6. DAILY SALES TREND
        daily_data = daily_sales_trend(transactions)
        file.write("DAILY SALES TREND\n")
        file.write("-" * 50 + "\n")
        file.write("Date         Revenue        Transactions  Customers\n")

        for date, data in daily_data.items():
            file.write(
                f"{date}  ₹{data['revenue']:,.2f}    "
                f"{data['transaction_count']}           "
                f"{data['unique_customers']}\n"
            )
        file.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        peak_day = find_peak_sales_day(transactions)
        low_products = low_performing_products(transactions)
        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 50 + "\n")
        file.write(f"Best Selling Day: {peak_day[0]} "
                   f"(₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n\n")

        file.write("Low Performing Products:\n")
        if low_products:
            for p in low_products:
                file.write(f"- {p[0]} (Qty: {p[1]}, Revenue: ₹{p[2]:,.2f})\n")
        else:
            file.write("None\n")
        file.write("\n")

        # 8. API ENRICHMENT SUMMARY
        enriched = [t for t in enriched_transactions if t["API_Match"]]
        not_enriched = [t for t in enriched_transactions if not t["API_Match"]]
        success_rate = (len(enriched) / len(enriched_transactions)) * 100
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 50 + "\n")
        file.write(f"Total Records Enriched: {len(enriched)}\n")
        file.write(f"Success Rate: {success_rate:.2f}%\n")
        file.write("Products Not Enriched:\n")

        for t in not_enriched:
            file.write(f"- {t['ProductID']} ({t['ProductName']})\n")

    print("Sales report generated:", output_file)
