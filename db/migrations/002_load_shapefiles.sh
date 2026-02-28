#!/bin/bash

echo "Current database: $POSTGRES_DB"
echo "Current user: $POSTGRES_USER"
env | grep -i postgres

DATA_DIR="/tmp/data"

# Unzip
unzip "${DATA_DIR}/tl_2025_28_tract.zip" -d "${DATA_DIR}/"

# Output shapefile to sql script using shp2pgsql shapefile loader, specifying table name
shp2pgsql -c -D -s 4269 -i -I "${DATA_DIR}/tl_2025_28_tract.shp" public.ms_tracts > /tmp/mstracts.sql

# Run sql script against db
psql -U postgres -d $POSTGRES_DB -f /tmp/mstracts.sql
