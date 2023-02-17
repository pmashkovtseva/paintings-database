SELECT paintings_schema.painting.id_painting, paintings_schema.painting.title, count(id_painting) exhibition_count
FROM paintings_schema.painting
LEFT JOIN paintings_schema.exhibition USING(id_painting) GROUP BY paintings_schema.painting.id_painting ORDER BY exhibition_count DESC