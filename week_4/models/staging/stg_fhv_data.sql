{{ config(materialized="view") }}

select 
-- identifiers
    {{ dbt_utils.surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as fhvid,
    dispatching_base_num,
    cast(PULocationID as integer) as pickup_location_id,
    cast(DOLocationID as integer) as dropoff_location_id,

-- timestamp
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,

-- trip info
    sr_flag,
    affiliated_base_number
from {{ source('staging', 'fhv_2019') }}
