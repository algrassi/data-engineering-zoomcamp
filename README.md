# Homework week 1

Exercises solutions:

1. docker build --help
2. Execute the following commands:
   1. docker run -it --entrypoint=bash python:3.9
   2. pip list
3. Go to [upload-data-green-taxi.ipynb](upload-data-green-taxi.ipynb) and [upload-data-zones.ipynb](upload-data-zones.ipynb)

## Query n.3

``` sql
SELECT COUNT(1)
FROM green_taxi_data as gtd
WHERE gtd.lpep_pickup_datetime::date = date '2019-01-15'
AND gtd.lpep_dropoff_datetime::date = date '2019-01-15';
```
## Query n.4

``` sql
SELECT gtd.lpep_pickup_datetime::date
FROM green_taxi_data as gtd
WHERE gtd.trip_distance = (SELECT MAX (gtd2.trip_distance) FROM green_taxi_data as gtd2);
```
## Query n.5

``` sql
SELECT '2' as passenger_count, count(*)
FROM green_taxi_data
WHERE lpep_pickup_datetime::date = date '2019-01-01' AND passenger_count = 2
UNION ALL
SELECT '3' as passenger_count, count(*)
FROM green_taxi_data
WHERE lpep_pickup_datetime::date = date '2019-01-01' AND passenger_count = 3;
```
## Query n.6

``` sql
SELECT "Zone"
SELECT "Zone" FROM zones WHERE "LocationID" = (
SELECT gtd."DOLocationID"
FROM green_taxi_data as gtd
JOIN zones as zns on zns."LocationID" = gtd."PULocationID"
WHERE zns."Zone" = 'Astoria'
ORDER BY gtd.tip_amount DESC LIMIT 1);
```
