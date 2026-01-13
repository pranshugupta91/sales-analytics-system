from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.report_generator import generate_sales_report

def main():
    """
    Main execution function
    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations
    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors
    """
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Show filter options
        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(t["Region"] for t in transactions))
        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{int(min(amounts))} - ₹{int(max(amounts))}")
        apply_filter = input("\nDo you want to filter data? (y/n): ").lower()
        if apply_filter == "y":
            region = input("Enter region (or press Enter to skip): ")
            min_amt = input("Enter minimum amount (or press Enter to skip): ")
            max_amt = input("Enter maximum amount (or press Enter to skip): ")
            region = region if region else None
            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None
            transactions, invalid_count, summary = validate_and_filter(
                transactions, region, min_amt, max_amt
            )
        else:
            transactions, invalid_count, summary = validate_and_filter(transactions)

        # 4. Validation summary
        print("\n[4/10] Validating transactions...")
        print(f"✓ Valid: {summary['final_count']} | Invalid: {invalid_count}")

        # 5. Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(transactions)
        region_wise_sales(transactions)
        top_selling_products(transactions)
        customer_analysis(transactions)
        daily_sales_trend(transactions)
        find_peak_sales_day(transactions)
        low_performing_products(transactions)
        print("✓ Analysis complete")

        # 6. API fetch
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrichment
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(transactions, product_mapping)
        enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
        success_rate = (enriched_count / len(enriched_transactions)) * 100
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} "
              f"transactions ({success_rate:.1f}%)")

        # 8. Save already done in enrich_sales_data
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 9. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n An error occurred.")
        print("Please check inputs or try again.")
        print("Error details:", e)

if __name__ == "__main__":
    main()
