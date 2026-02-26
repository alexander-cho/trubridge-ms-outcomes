#From the terminal, or skip first command if going from Docker container exec:
#```shell
#docker exec -it trubridge-db sh
#```
#Install `unzip` for Debian-based container image
#```shell
#apt-get update && apt-get install -y unzip
#```
#Unzip
#```shell
#unzip tmp/tl_2025_28_tract.zip
#```
#Output shapefile to sql script using shp2pgsql shapefile loader, specifying table name
#```shell
#shp2pgsql -c -D -s 4269 -i -I tl_2025_28_tract.shp public.ms_tracts > mstracts.sql
#```
#Run sql script against db
#```shell
#psql -U postgres -d trubridge-ms-outcomes-db -f mstracts.sql
#```