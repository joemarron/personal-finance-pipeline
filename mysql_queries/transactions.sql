WITH ranked_data AS (
  SELECT
    t.transaction_id,
    t.booking_date,
    b.bank,
    t.description_text,
    t.amount,
    t.subcategory_id,
    ROW_NUMBER() OVER (PARTITION BY EXTRACT(YEAR FROM booking_date), EXTRACT(MONTH FROM booking_date), subcategory_id ORDER BY booking_date) AS row_num
  FROM
    transactions AS t
    LEFT JOIN subcategories AS sc ON sc.subcategory_id = t.subcategory_id
    LEFT JOIN categories AS c ON c.category_id = sc.category_id
    LEFT JOIN accounts AS a ON a.account_id = t.account_id
    LEFT JOIN banks AS b ON b.account_id = a.account_id
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
  
ORDER BY 2;

