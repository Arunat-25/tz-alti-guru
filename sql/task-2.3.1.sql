DROP VIEW IF EXISTS top_5_products_last_month;
CREATE VIEW top_5_products_last_month AS
SELECT 
    p.name AS product_name,
    root.name AS top_category,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN orders o ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
JOIN LATERAL (
    WITH RECURSIVE category_path AS (
        SELECT id, parent_id, name
        FROM categories 
        WHERE id = p.category_id
        
        UNION ALL
        
        SELECT c.id, c.parent_id, c.name
        FROM categories c
        JOIN category_path cp ON c.id = cp.parent_id
    )
    SELECT name 
    FROM category_path 
    WHERE parent_id IS NULL
    LIMIT 1
) root ON true
WHERE o.created_at >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY p.id, p.name, root.name
ORDER BY total_sold DESC
LIMIT 5;