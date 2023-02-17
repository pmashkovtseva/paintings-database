SELECT title, name, dates, locality, country
FROM paintings_schema.exhibition, paintings_schema.museum, paintings_schema.location
WHERE paintings_schema.exhibition.id_museum = paintings_schema.museum.id_museum AND paintings_schema.museum.id_location = paintings_schema.location.id_location AND paintings_schema.location.country LIKE 'Germany'
