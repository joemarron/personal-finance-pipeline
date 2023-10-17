# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 11:50:02 2023

@author: joema
"""

import os
import dotenv
from sqlalchemy import create_engine, text
import pandas as pd

dotenv.load_dotenv('./airflow-docker/dags/.env')
fullstring = os.getenv('DATABASE_URL')

engine = create_engine(fullstring)


uncat_trans = './categorisation/uncategorised_transactions.sql'
with open(uncat_trans, 'r') as file:
    sql_script = file.read()
uncat_df = pd.read_sql(sql_script, engine)

category_path = './categorisation/category_list.sql'
with open(category_path, 'r') as file:
    sql_script = file.read()
cat_lkp = pd.read_sql(sql_script, engine)

mapping_df = pd.read_sql('SELECT * FROM "#mapping"', engine)


if len(uncat_df) > 0:
    mapping_updates = []
    transac_updates = []
    
    print("# ~~~~~~~~~~~~~~~~ CATEGORY LOOKUP ~~~~~~~~~~~~~~~~ #")
    print(cat_lkp[['category_name', 'subcategory_name', 'subcategory_id']])
    print("# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #")
    
    print('\nCATEGORISE THE FOLLOWING TRANSACTIONS:')
    print('--------------------------------------')
    print('Indicate the subcategory_id for each of the trnasactions:')
    for i, x in uncat_df.iterrows():
        user_subcat_id = input('%s (%s):' %(x['description_text'], x['amount']))
        mapping_updates.append([x['description_text'], user_subcat_id])
        transac_updates.append([x['transaction_id'], user_subcat_id])
        
    insert_query = """INSERT INTO "#mapping" (description_text, subcategory_id) VALUES ('%s', %s);"""
    for line in mapping_updates:
        new_value1, new_value2 = line[0], line[1]
        with engine.begin() as connection:
            connection.execute(text(insert_query % (new_value1, new_value2)))
            
    transac_query = "UPDATE transactions SET subcategory_id = %s WHERE transaction_id = %s"
    for line in transac_updates:
        primary_key_value, new_value = line[0], line[1]
        with engine.begin() as connection:
            connection.execute(text(transac_query % (new_value, primary_key_value)))     
    
    print('--------------------------------------')
    print('---TRANSACTIONS MAPPED//CATEGORISED---')

else:
    print('All TRANSACTIONS ALREADY CATEGORISED.')



engine.dispose()