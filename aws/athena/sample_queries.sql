-- create table from clouwatch log files. format is jsonl.
-- with partition setting
CREATE EXTERNAL TABLE IF NOT EXISTS default.tmp_log (
  `logStream` string,
  `logEvents` array<struct<timestamp: timestamp, message:string>>
)
PARTITIONED BY (`orderdate` string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES ('serialization.format' = '1' )
LOCATION 's3://YOUR_BUCKET/'
TBLPROPERTIES (
  'has_encrypted_data'='false',
  'projection.enabled' = 'true',
  'projection.orderdate.type' = 'date',
  'projection.orderdate.range' = '2020/09/27,NOW',
  'projection.orderdate.format' = 'yyyy/MM/dd',
  'projection.orderdate.interval' = '1',
  'projection.orderdate.interval.unit' = 'DAYS',
  'storage.location.template' = 's3://<MY_BUCKET>/${orderdate}',
  'classification'='json',
  'compressionType'='gzip',
  'typeOfData'='file'
 );


-- unnest array
SELECT logStream, e.message FROM tmp_log CROSS JOIN UNNEST(logEvents) as t(e)
where logstream = '<YOUR_STREAM_NAME>';

-- get last element of array filtered out null
SELECT logStream, element_at(array_agg(logEvents) FILTER (WHERE logEvents IS NOT NULL), -1) AS logEvent
FROM tmp_log
group by logStream;


-- get using partition effectively (range is 5 days ago ~ 3 days ago)
select * from tmp_log
where cast(date_parse(orderdate, '%Y/%m/%d') as date)
  between current_date - interval '5' day
  and current_date - interval '3' day
