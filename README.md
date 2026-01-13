# Sales Analytics System
## Project Overview
The **Sales Analytics System** is an end-to-end Python-based data analytics application.

It performs:
- Sales data parsing, cleaning, and validation
- Business analytics using Python lists, dictionaries, and functions
- External API integration using DummyJSON
- Data enrichment and reporting
- Automated text report generation

## Project Structure
```
sales-analytics-system/
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
├── utils/
│   ├── data_processor.py
│   ├── api_handler.py
│   └── file_handler.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run
From the root directory, run:
```
python main.py
```
## Output Files Generated
After successful execution:
- `data/enriched_sales_data.txt` → Sales data enriched with API product details
- `output/sales_report.txt` → Comprehensive analytics report

## Key Features
- Robust data validation & filtering
- Region-wise, product-wise, and customer-wise analytics
- API-based product enrichment
- Graceful error handling
- Clean, evaluator-friendly console logs
- No hardcoded file paths