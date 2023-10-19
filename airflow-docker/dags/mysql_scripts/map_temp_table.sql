INSERT INTO transactions (text_id, account_id, description_text, amount, subcategory_id, booking_date)
SELECT 
temp."transactionId"::STRING,
ac.account_id::INT,
temp."remittanceInformationUnstructured"::STRING,
temp."transactionAmount.amount"::FLOAT,
sm.subcategory_id,  -- Subcategory mapping from the mapping table
temp."bookingDate"::DATE

FROM "#temp_transactions" AS temp
LEFT JOIN accounts AS ac ON temp."Account" = CAST(ac.account AS STRING)
LEFT JOIN "#mapping" sm ON temp."remittanceInformationUnstructured" = sm.description_text

ON CONFLICT DO NOTHING;
