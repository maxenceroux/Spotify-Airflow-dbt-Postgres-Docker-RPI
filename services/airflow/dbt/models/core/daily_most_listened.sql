with source_data as (

    select artist, count(*) nb_plays
    from {{source('spotify_models', 'listen')}}
    left join {{source('spotify_models', 'song')}} using(spotify_id)
    where artist is not null
    group by artist order by count(*) desc limit 5

)

select *
from source_data

