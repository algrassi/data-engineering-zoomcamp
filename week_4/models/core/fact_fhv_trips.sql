{{ config(materialized='table') }}

with dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
),

fhv_trips as (
    select * from {{ ref('stg_fhv_data')}}
)
select 
    fhv_trips.dispatching_base_num,
    fhv_trips.pickup_location_id,
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    fhv_trips.dropoff_location_id,
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
    fhv_trips.pickup_datetime, 
    fhv_trips.dropoff_datetime, 
    fhv_trips.sr_flag, 
    fhv_trips.affiliated_base_number, 
from fhv_trips
inner join dim_zones as pickup_zone
on fhv_trips.pickup_location_id = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_trips.dropoff_location_id = dropoff_zone.locationid
