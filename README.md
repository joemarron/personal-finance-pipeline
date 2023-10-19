
# Personal Finance

***Any transaction values used in this repo has been fabricated for privacy reasons.***

This repo documents the pipeline built to download and manage our personal finances. I have utilised [GoCardless (Formerly Nordigen)](https://gocardless.com/bank-account-data/) API to extract transactions using Python and managed the pipeline and data storage with Apache-Airflow and CockroachDB. The below diagram demonstrates the implemented data pipeline. 

![pipeline](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/data_pipeline.png)


## Data Model
The schema design below shows how the CockroachDB database was set up. Transactions descriptions *(text_id)* are mapped to subcategories in the mapping table. These are used to categorise new transactions. The data pipeline leaves the subcategory_id blank if its not found in the mapping table. Seperately run python scripts are run where I can categorise any uncategorised transactions in the database, adding the associated descriptions to the mapping table. The database contains a coupel years of categorised transactions, so this doesn't need to be done too often, with a handful of uncategorised transactions expected over any given month.
![db_schema](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/schema.png)

## ETL Pipeline
![airflow_png](https://github.com/joemarron/personal-finance-pipeline/blob/main/misc/AIRFLOW_DAG.png)
