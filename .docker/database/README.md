# Cassandra

## Docker build & Run

```bash
$ make build_db run_db
$ docker logs -f database
<logs will print out ....  wait for line below to show up>
INFO  [OptionalTasks:1] 2023-04-06 23:39:36,153 CassandraRoleManager.java:374 - Created default superuser role 'cassandra'

$ export DB_USER=cassandra
$ export DB_PWD=cassandra
$ docker exec -it database bash -c "cqlsh -u $DB_USER -p $DB_PWD"

cassandra@cqlsh> EXPAND ON;
<formats terminal viewing quite nicely>

cassandra@cqlsh> SHOW VERSION;
cassandra@cqlsh> DESCRIBE KEYSPACES;
cassandra@cqlsh> SELECT * FROM system_schema.keyspaces;
cassandra@cqlsh> USE decoder;
cassandra@cqlsh:fusion> DESCRIBE TABLES;
cassandra@cqlsh:fusion> SELECT COUNT(*) FROM decoder.capture;
```