
# Personal Finance

***Any transaction values used in this repo has been fabricated for privacy reasons.***

This repo documents the pipeline built to download and manage our personal finances. I have utilised [GoCardless (Formerly Nordigen)](https://gocardless.com/bank-account-data/) API to extract transactions using Python and managed the pipeline and data storage with Apache-Airflow and CockroachDB. The below diagram demonstrates the implemented data pipeline. 

![pipeline](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/data_pipeline.png)


## Data Model
The schema design below shows how the CockroachDB database was set up. Transactions descriptions *(description_text)* are mapped to subcategories in the mapping table. These are used to categorise new transactions. The data pipeline leaves the subcategory_id blank if its not found in the mapping table. Seperately run python scripts are run where I can categorise any uncategorised transactions in the database, adding the associated descriptions to the mapping table. The database contains a coupel years of categorised transactions, so this doesn't need to be done too often, with a handful of uncategorised transactions expected over any given month.
![db_schema](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/schema.png)

## ETL Pipeline
Apache-Airflow has been utilised to automate the transaction inserts into the CockroachDB database on a daily basis at 7:00am. This process automates the following tasks:
1. Extract transactions for given bank accounts.
2. Upload transactions into database ***#temp*** table.
3. Transform ***#temp*** table rows into transaction tables, inserting appropriate subcategory_id
4. Check and remove any duplicated rows based on the ***text_id*** column value

![airflow_png](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/AF_DAG.png)

## Power BI Report
The below shows a version of the Power BI report created to track both current month expenditure against budgets and overall net worth, **with fabricated data**.
![airflow_png](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/POWERBI_DASHBOARD_EXAMPLE.png)
