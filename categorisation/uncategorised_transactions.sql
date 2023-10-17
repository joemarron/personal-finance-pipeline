SELECT
t.*
FROM transactions AS t
WHERE t.subcategory_id IS NULL;
