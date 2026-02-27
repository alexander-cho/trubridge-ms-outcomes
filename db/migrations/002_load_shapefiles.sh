##!/bin/bash
#
#
#cd /tmp/data
#
## Unzip
#unzip tl_2025_28_tract.zip
#
## Output shapefile to sql script using shp2pgsql shapefile loader, specifying table name
#shp2pgsql -c -D -s 4269 -i -I tl_2025_28_tract.shp public.ms_tracts > /tmp/mstracts.sql
#
## Run sql script against db
#psql -U postgres -d trubridge-ms-outcomes-db -f /tmp/mstracts.sql
