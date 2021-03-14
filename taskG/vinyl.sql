SELECT
	musicians.name,
    labels.name,
    albums.name,
    albums.rating
FROM
	albums
JOIN
labels
	ON albums.label_id=labels.id
JOIN
musicians
	ON albums.musician_id=musicians.id
WHERE
	(albums.rating < 10 AND albums.rating > 4)
    AND
    (labels.name = "Граммофон" OR labels.name = "Скрипичный ключ")
ORDER BY
	musicians.name ASC
;
