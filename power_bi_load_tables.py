# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 20:23:23 2023

@author: joema
"""

import os
import dotenv
from sqlalchemy import create_engine, text
import pandas as pd

dotenv.load_dotenv('./airflow-docker/dags/.env')
fullstring = os.getenv('DATABASE_URL')

engine = create_engine(fullstring)
conn = engine.connect()


trans_resp = conn.execute(text("""
  WITH ranked_data AS (
  SELECT
    t.transaction_id,
    t.booking_date,
    b.bank,
    t.description_text,
    t.amount,
    t.subcategory_id,
    ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM booking_date), EXTRACT(MONTH FROM booking_date), t.subcategory_id ORDER BY booking_date) AS row_num
  FROM
    transactions AS t
    LEFT JOIN subcategories AS sc ON sc.subcategory_id = t.subcategory_id
    LEFT JOIN categories AS c ON c.category_id = sc.category_id
    LEFT JOIN accounts AS a ON a.account_id = t.account_id
    LEFT JOIN banks AS b ON b.bank_id = a.bank_id
)
SELECT
    r.transaction_id,
    r.booking_date,
    r.bank,
    r.description_text,
    r.amount,
    r.subcategory_id,
  CASE
    WHEN subcategory_id = 1 AND row_num = 1 THEN 1
    ELSE 0
  END AS new_month
FROM
  ranked_data r
  
ORDER BY 2;""")).fetchall()

transactions = pd.DataFrame(trans_resp, columns=['transaction_id', 'booking_date', 'bank', 'description',
                               'amount', 'subcategory_id', 'new_month'])

print(transactions)

transactions.to_csv('trans.csv')

bdgts_resp = conn.execute(text("""SELECT * FROM budgets;""")).fetchall()

budgets = pd.DataFrame(bdgts_resp, columns=['budget_id', 'subcategory_id', 'budget_amount', 'start_date', 'end_date'])

print(budgets)

subcat_resp = conn.execute(text("""SELECT * FROM subcategories;""")).fetchall()

subcategories = pd.DataFrame(subcat_resp, columns=['subcategory_id','subcategory', 'category_id'])

print(subcategories)

cat_resp = conn.execute(text("""SELECT * FROM categories;""")).fetchall()

categories = pd.DataFrame(cat_resp, columns=['category_id','category'])

print(categories)