INSERT INTO transactions (text_id, account_id, booking_date, description_text, amount, subcategory_id)
SELECT 
temp."transactionId",
ac.account_id::FLOAT,
temp."bookingDate",
temp."remittanceInformationUnstructured",
temp."transactionAmount.amount"::FLOAT,
sm.subcategory_id::INTEGER  -- Subcategory mapping from the mapping table
    
FROM "#temp_transactions" AS temp
LEFT JOIN accounts AS ac ON temp."Account" = ac.account
LEFT JOIN "#mapping" sm ON temp."remittanceInformationUnstructured" = sm.description_text

ON CONFLICT DO NOTHING;
