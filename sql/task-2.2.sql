WITH RECURSIVE descendants AS (
    SELECT 
        c.id,
        c.parent_id AS root_id
    FROM categories c
    WHERE c.parent_id IN (SELECT id FROM categories WHERE parent_id IS NULL)
    
    UNION ALL
    
    SELECT 
        c.id,
        d.root_id
    FROM categories as c
    JOIN descendants as d 
    ON c.parent_id = d.id
)
SELECT 
    root.name AS category_name,
    COUNT(d.id) AS total_descendants
FROM descendants d
JOIN categories as root 
ON d.root_id = root.id
GROUP BY root.id, root.name
ORDER BY total_descendants DESC;