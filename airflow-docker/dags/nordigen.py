# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 10:23:59 2023

@author: joema
"""

def get_transactions():
    import requests
    from requests.structures import CaseInsensitiveDict
    import json
    import pandas as pd
    import webbrowser
    import time
    import datetime as dt
    import os
    import dotenv

    dotenv.load_dotenv()
    
    # TOKENS & IDS
    secret_id       = os.getenv('SECRET_ID')
    secret_key      = os.getenv('SECRET_KEY')
    token           = os.getenv('TOKEN')
    refresh_token   = os.getenv('REFRESH_TOKEN')
    account_keys    = ['ACCOUNT_ID_HSBC', 'ACCOUNT_ID_STLG']
    account_id_HSBC = os.getenv('ACCOUNT_ID_HSBC')
    account_id_STLG = os.getenv('ACCOUNT_ID_STLG')
    bank_code_HSBC  = os.getenv('BANK_CODE_HSBC')
    bank_code_STLG  = os.getenv('BANK_CODE_STLG')
    
    #REQUIRED IDENTIFIERS
    bank_codes = [bank_code_HSBC, bank_code_STLG]
    bank_ids = [account_id_HSBC, account_id_STLG]
    
    # REQUIRED URLs
    url_token   = "https://ob.nordigen.com/api/v2/token/new/"
    url_refresh = "https://ob.nordigen.com/api/v2/token/refresh/"
    url_banks   = "https://ob.nordigen.com/api/v2/institutions/?country=gb"
    url_reqs    = "https://ob.nordigen.com/api/v2/requisitions/"
    url_accs    = 'https://ob.nordigen.com/api/v2/requisitions/%s/'
    url_trans   = "https://ob.nordigen.com/api/v2/accounts/{account_id}/transactions/"
    url_details = "https://ob.nordigen.com/api/v2/accounts/{id}/details/"
    

    # HEADERS
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = token
    
    # USER SECRETS
    secrets ='{"secret_id":"%s", "secret_key":"%s"}' % (secret_id, secret_key)
     
    
    # ~~~~~~~~~~~~~~~~~~~ TEST API RESPONSE ~~~~~~~~~~~~~~~~~~~ #
    bank_resp = requests.get(url_banks, headers=headers)

    # GET NEW TOKEN IF EXPIRED
    if bank_resp.status_code != 200:
        refresh = '{"refresh":"' + refresh_token + '"}'
           
        try: # GET NEW TOKEN USING REFRESH TOKEN
            get_new_token = requests.post(url_refresh, headers=headers, data=refresh)
            auth_dict = get_new_token.json()
            token = "Bearer " + auth_dict['access']
            dotenv.set_key(dotenv_path='.env', key_to_set="TOKEN", value_to_set=token)
            
            headers["Authorization"] = token
            
        except: # OR GET NEW TOKEN FROM STRATCH
            get_new_token = requests.post(url_token, headers=headers, data=secrets)
            new_access_token = "Bearer " + get_new_token.json()['access']
            dotenv.set_key(dotenv_path='.env', key_to_set="TOKEN", value_to_set=new_access_token)
            new_refresh_token = get_new_token.json()['refresh']
            dotenv.set_key(dotenv_path='.env', key_to_set="REFRESH_TOKEN", value_to_set=new_refresh_token)
    
            headers["Authorization"] = new_access_token
      
    # ~~~~~~~~~~~~~~~~~~~~ GET TRANSACTIONS ~~~~~~~~~~~~~~~~~~~ #
    trans_cols = ['Bank','Account', 'transactionId', 'bookingDate', 'valueDate', 'proprietaryBankTransactionCode', 
                  'remittanceInformationUnstructured', 'creditorName', 'additionalInformation', 'entryReference',
                  'transactionAmount.amount','transactionAmount.currency']
    transactions = pd.DataFrame(columns=trans_cols)
    
    # GET TRANSACTIONS FOR EACH BANK
    file = 0
    for _id_ in bank_codes:
        
        # GET TRANSACTIONS
        trans = requests.get(url_trans.format(account_id=bank_ids[file]), headers=headers)
    
        # IF RESPONSE ERROR THEN MANUAL REFRESH
        if trans.status_code != 200:
            print("Error - Needs Manual Refresh")
            
            #GET REQ ID
            req_data = '{"redirect": "http://www.google.com/","institution_id": "%s"}' % _id_
            req_resp = requests.post(url_reqs, headers=headers, data=req_data)
            req_json = req_resp.json()
            req_str = json.dumps(req_json)
            req_obj = json.loads(req_str)
            
            # OPEN LINK TO USER ACCOUNT LOGIN
            webbrowser.open(req_obj["link"])
           
            # WAIT FOR USER LOGIN
            time.sleep(120)
           
            # GET ACCOUNTS
            acc_list = requests.get(url_accs % req_obj["id"], headers=headers)
            acc_json = acc_list.json()
            acc_str = json.dumps(acc_json)
            acc_obj = json.loads(acc_str)  
            print(acc_obj)
            account_id = acc_obj['accounts'][0]
            dotenv.set_key(dotenv_path='.env', key_to_set=account_keys[file], value_to_set=account_id)
           
            # GET TRANSACTIONS WITH NEW ACCOUNT ID
            trans = requests.get(url_trans.format(account_id=account_id), headers=headers)
            
        # FORMAT TRANSACTIONS AND GET APPEND ACCOUNT DETAILS    
        trans_js = trans.json()
        details = requests.get(url_details.format(id=bank_ids[file]), headers=headers)
        details_js = details.json()
        trans_df = pd.json_normalize(trans_js, record_path =['transactions', 'booked'])
        trans_df['Bank'] = _id_
        trans_df['Account'] = details_js['account']['bban']
        transactions = pd.concat([transactions, trans_df])
        
        file += 1
        
    # WRITE NEW TRANSACTIONS TO FILE    
    #transactions.to_csv('testing_hsbc_and_starling.csv')
    
    # REFORMAT SPLIT
    for col in ['remittanceInformationUnstructured', 'additionalInformation', 'entryReference']:
        transactions[col] = transactions[col].apply(lambda x: " ".join(str(x).split()))
    
    
    return transactions


if __name__ == "__main__":
    get_transactions()

        

