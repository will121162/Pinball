# Pinball
This is a software project with multiple steps, with the ultimate goal of writing the embedded code for a pinball machine. This makes use of classes and simple data structures.

this also opens the option for post game analysis, given the simulation and the embedded solution write /will write to a mysql server with session specific metrics.

## SQL schema;
```sql
+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| session_id  | int         | NO   | PRI | NULL    | auto_increment |
| player_name | varchar(50) | NO   |     | NULL    |                |
+-------------+-------------+------+-----+---------+----------------+
2 rows in set (0.00 sec)

mysql> describe events;
+------------+-----------+------+-----+-------------------+-------------------+
| Field      | Type      | Null | Key | Default           | Extra             |
+------------+-----------+------+-----+-------------------+-------------------+
| event_id   | int       | NO   | PRI | NULL              | auto_increment    |
| session_id | int       | NO   | MUL | NULL              |                   |
| pin_id     | int       | NO   |     | NULL              |                   |
| created_at | timestamp | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| event_time | text      | NO   |     | NULL              |                   |
+------------+-----------+------+-----+-------------------+-------------------+
5 rows in set (0.01 sec)
```

sql specific functions;

SQL_init:
    initalises new session_id by uploading player name to 'sessions' table
    each session has a unique session_id

SQL_upload:
    sends game data from MC to mySQL sever such as;
        pin_id
        datetime

the python system example now works as expected, example sql data;
```sql
mysql> select * from events where session_id = 18 limit 5;
+----------+------------+--------+---------------------+----------------------------+
| event_id | session_id | pin_id | created_at          | event_time                 |
+----------+------------+--------+---------------------+----------------------------+
|     2221 |         18 |      2 | 2026-11-27 00:38:54 | 2026-11-27 00:38:54.648420 |
|     2222 |         18 |      3 | 2026-11-27 00:38:54 | 2026-11-27 00:38:54.648420 |
|     2223 |         18 |      7 | 2026-11-27 00:38:54 | 2026-11-27 00:38:54.648420 |
|     2224 |         18 |     50 | 2026-11-27 00:38:54 | 2026-11-27 00:38:54.648420 |
|     2225 |         18 |      1 | 2026-11-27 00:38:54 | 2026-11-27 00:38:54.690308 |
+----------+------------+--------+---------------------+----------------------------+

mysql> select * from sessions;
+------------+-------------+
| session_id | player_name |
+------------+-------------+
|         16 | test_user   |
|         17 | test_user   |
|         18 | test_user   |
+------------+-------------+


```