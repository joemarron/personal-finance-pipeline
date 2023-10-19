SELECT
tbl.*,
(ROUND(tbl.subcat_cumsum - tbl.budget_amount, 2) AS 'budet_remaining'


FROM (
SELECT
t2.transaction_id,
ROUND(CASE
	WHEN t2.custom_sequence % 2 != 0 THEN ((t2.custom_sequence + 1)/2)
	ELSE (t2.custom_sequence / 2)
END) AS 'budget_month',
YEAR(t2.booking_date) AS 'year',
MONTH(t2.booking_date) AS 'month',
ba.bank,
t2.booking_date, 
t2.description_text,
s.subcategory_name AS 'subcategory',
c.category_name AS 'category',
t2.amount,
ROUND(SUM(ROUND(SUM(t2.amount),2)) over (PARTITION BY ROUND(CASE WHEN t2.custom_sequence % 2 != 0 THEN ((t2.custom_sequence + 1)/2) ELSE (t2.custom_sequence / 2)
END), t2.subcategory_id ORDER BY t2.booking_date), 2) AS subcat_cumsum,
b.budget_amount


FROM (SELECT
    t.*,
    (@counter := IF(t.subcategory_id = 1, @counter + 1, @counter)) AS custom_sequence
FROM
    (SELECT *, @counter := 0 FROM transactions ORDER BY booking_date) AS t) AS t2
    LEFT JOIN subcategories AS s ON s.subcategory_id = t2.subcategory_id
    LEFT JOIN budgets as b ON s.subcategory_id = b.subcategory_id
    LEFT JOIN categories AS c ON c.category_id = s.category_id
    LEFT JOIN accounts AS a ON a.account_id = t2.account_id
    LEFT JOIN banks AS ba ON ba.account_id = a.account_id
    
GROUP BY t2.transaction_id
ORDER BY YEAR(t2.booking_date), MONTH(t2.booking_date), c.category_name, s.subcategory_id, t2.booking_date
) AS tbl

ORDER BY tbl.budget_month, tbl.category, tbl.subcategory, tbl.booking_date