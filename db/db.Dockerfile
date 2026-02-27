FROM postgis/postgis:17-3.5 AS builder
RUN apt update
RUN apt install -y postgis
RUN which shp2pgsql


FROM postgis/postgis:17-3.5

COPY --from=builder /usr/bin/shp2pgsql /usr/bin/shp2pgsql

RUN #apt-get update && apt-get install -y unzip

COPY migrations/ /docker-entrypoint-initdb.d/
COPY data/ /tmp/data/

#RUN chmod +x /docker-entrypoint-initdb.d/*.sh
#RUN chown -R postgres:postgres /tmp/data/

# check shp2pgsql is installed
RUN shp2pgsql