# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:53:48 2023

@author: joema
"""


def add_transactions_to_temp():
    import os
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, text
    from nordigen import get_transactions
    from datetime import datetime
    #import pandas as pd
    
    load_dotenv()
    fullstring = os.getenv('DATABASE_URL')
    
    engine = create_engine(fullstring)
    conn = engine.connect()
    
    q_date = conn.execute(text("SELECT MAX(t.booking_date) FROM transactions t;")).fetchall()[0][0]
    t_date = datetime.now().date()
    
    if q_date < t_date:
        df = get_transactions()
        
        filtered_cols = ['Bank','Account', 'transactionId', 'bookingDate',
                         'remittanceInformationUnstructured','transactionAmount.amount']
        df = df[filtered_cols]
    
        df.to_sql('#temp_transactions', con=engine, if_exists='replace', index=False)
    
    # Close the engine
    engine.dispose()
    
def transform_transactions_into_db():
    #import pandas as pd
    import os
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, text
    
    load_dotenv()
    fullstring = os.getenv('DATABASE_URL')
    
    engine = create_engine(fullstring)
    
    map_script_path = './dags/mysql_scripts/map_temp_table.sql'
    del_temp_script = './dags/mysql_scripts/delete_temp_table.sql'
    check_dup_path  = './dags/mysql_scripts/check_duplicates.sql'    
    
    with open(map_script_path, 'r') as map_file:
        map_script = map_file.read()
    with open(del_temp_script, 'r') as del_file:
        del_script = del_file.read()
    with open(check_dup_path, 'r') as dup_file:
        dup_script = dup_file.read()    
    with engine.begin() as connection:
            connection.execute(text(map_script))   
            connection.execute(text(del_script))
            connection.execute(text(dup_script))
            
    engine.dispose()      
    
    
    
