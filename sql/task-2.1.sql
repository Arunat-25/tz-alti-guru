SELECT 
    c.name as client_name, 
    COALESCE(SUM(oi.quantity), 0) as products_quantity,
    COALESCE(SUM(oi.quantity * oi.price_at_order), 0) as total_amount
FROM order_items as oi 
JOIN orders as o
ON oi.order_id = o.id
RIGHT JOIN clients as c
ON o.client_id = c.id
GROUP BY c.id, c.name
ORDER BY total_amount DESC