SELECT
sc.*,
c.category_name
FROM subcategories AS sc
LEFT JOIN categories AS c ON c.category_id = sc.category_id;
