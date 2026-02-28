# Manually uploading shapefiles to a Docker container and converting to SQL dump for PostGIS v.s. Mounting a script

### (TODO)

___

Getting the shapefiles data into the PostGIS database. This will likely become a script to run automatically.

From the terminal, or skip first command if going from Docker container exec:
```shell
docker exec -it trubridge-db sh
```
Install `unzip` for Debian-based container image
```shell
apt-get update && apt-get install -y unzip
```
Unzip
```shell
unzip /tmp/data/tl_2025_28_tract.zip -d /tmp/data/
```
Output shapefile to SQL script using shp2pgsql shapefile loader, specifying table name
```shell
shp2pgsql -c -D -s 4269 -i -I /tmp/data/tl_2025_28_tract.shp public.ms_tracts > mstracts.sql
```
Run sql script against db
```shell
psql -U postgres -d trubridge-ms-outcomes-db -f mstracts.sql
```

To exit the Docker shell: `Ctrl(^) + P` then `Ctrl(^) + Q`