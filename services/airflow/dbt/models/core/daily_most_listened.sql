with source_data as (

    select artist, count(*) nb_plays
    from {{source('spotify_models', 'song')}}
    group by artist order by count(*) desc limit 5

)

select *
from source_data

