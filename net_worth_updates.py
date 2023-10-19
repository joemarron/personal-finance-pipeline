# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:48:55 2023

@author: joema
"""

import pandas as pd

networth_df = pd.read_csv('net_worths.csv')

values = []
for i, x in networth_df.iterrows():
    if x['Category'] == "Home Equity":
        home_valuation = float(input('Current house evaluation: £'))
        mortgage_bal   = float(input('Remaining Mortgage Balance: £'))
        values.append(round(home_valuation-mortgage_bal, 2))
    else:
        input_bal = float(input('%s: £' % x['Category']))
        values.append(round(input_bal, 2))
    
networth_df['Value'] = values

networth_df.to_csv('net_worths.csv', index=False)