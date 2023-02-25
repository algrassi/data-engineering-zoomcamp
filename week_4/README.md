# WEEK-4 HOMEWORK

## Query 1
``` sql
SELECT COUNT(*) FROM `helical-ascent-375912.production.fact_trips`;
```
For this query the result is: 61540940

## Query 2
``` sql
SELECT COUNT(*) FROM `helical-ascent-375912.dbt_agrassi.stg_fhv_data`
WHERE EXTRACT(ISOYEAR FROM pickup_datetime) = 2019
```
For this query the result is: 43120566

## Query 3
``` sql
SELECT COUNT(*) FROM `helical-ascent-375912.dbt_agrassi.fact_fhv_trips`
WHERE EXTRACT(ISOYEAR FROM pickup_datetime) = 2019
```
For this query the result is: 22978577

## Question number 2 and 5
You can find the pdf reports in the same folder of this README.md file
