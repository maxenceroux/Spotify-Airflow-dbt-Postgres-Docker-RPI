with source_data as (

select 
	extract(isodow from ts) day_of_week,
	extract(hour from ts) as hour,
	count(*) nb
from {{source('spotify_models', 'song')}}
group by day_of_week, hour
order by nb desc

)

select *
from source_data

