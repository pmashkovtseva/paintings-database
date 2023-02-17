SELECT artist_name, title, creation_date from (
					SELECT paintings_schema.painting.title,
                          creation_date,
                          paintings_schema.artist.name artist_name,
                          paintings_schema.museum.name museum_name,
                          paintings_schema.medium.title medium_title,
                          paintings_schema.art_movement.title art_movement_title
                   FROM paintings_schema.painting,
                        paintings_schema.artist,
                        paintings_schema.museum,
                        paintings_schema.medium,
                        paintings_schema.art_movement
                   WHERE paintings_schema.painting.id_artist = paintings_schema.artist.id_artist
                     AND paintings_schema.painting.id_museum = paintings_schema.museum.id_museum
                     AND paintings_schema.painting.id_medium = paintings_schema.medium.id_medium
                     AND paintings_schema.painting.id_art_movement = paintings_schema.art_movement.id_art_movement
                   ORDER BY paintings_schema.painting.title
                   )
AS painting_metadata WHERE creation_date LIKE '20%'