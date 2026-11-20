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