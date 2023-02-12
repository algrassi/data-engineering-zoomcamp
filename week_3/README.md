# WEEK-3 HOMEWORK

## Query 1
``` sql
CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp.ext_fhv_2019`
OPTIONS (
  format = 'CSV',
  uris = ['gs://week_3_homework/data/fhv/fhv_tripdata_2019-*.csv.gz']
);

CREATE OR REPLACE TABLE `dezoomcamp.int_fhv_2019` AS
SELECT * FROM `dezoomcamp.ext_fhv_2019`;

SELECT count(*)
FROM `dezoomcamp.int_fhv_2019`;
```
For this query the result is: 43244696

## Query 2
```sql
SELECT DISTINCT ext.Affiliated_base_number FROM `dezoomcamp.ext_fhv_2019` AS ext;

SELECT DISTINCT int.Affiliated_base_number FROM `dezoomcamp.int_fhv_2019` AS int;
```
The first one (External) 0 Byte
The second one (Internal) 317,94 Byte

## Query 3
```sql
SELECT COUNT(*) FROM `dezoomcamp.int_fhv_2019` AS ext WHERE ext.PUlocationID is NULL AND ext.DOlocationID is NULL;
```
Result for this one is: 717.748

## Query 4
```sql
CREATE OR REPLACE TABLE `dezoomcamp.clust_fhv_2019`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS
SELECT * FROM `dezoomcamp.ext_fhv_2019`;
```

## Query 5
```sql
SELECT DISTINCT ext.Affiliated_base_number FROM `dezoomcamp.int_fhv_2019` AS ext 
WHERE DATE(ext.pickup_datetime) BETWEEN DATE(2019, 03, 01) AND DATE(2019, 03, 31);

SELECT DISTINCT ext.Affiliated_base_number FROM `dezoomcamp.clust_fhv_2019` AS ext 
WHERE DATE(ext.pickup_datetime) BETWEEN DATE(2019, 03, 01) AND DATE(2019, 03, 31);
```
The first one (External) 647,87 MB
The second one (Internal) 23,05 MB









