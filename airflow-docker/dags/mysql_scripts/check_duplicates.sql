DELETE FROM transactions a
        USING transactions b
WHERE
    a.transaction_id < b.transaction_id
    AND a.text_id = b.text_id;