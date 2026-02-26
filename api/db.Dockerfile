FROM postgis/postgis:17-3.5 as builder
RUN apt update
RUN apt install -y postgis
RUN which shp2pgsql

FROM postgis/postgis:17-3.5

COPY --from=builder /usr/bin/shp2pgsql /usr/bin/shp2pgsql

# check shp2pgsql is installed
RUN shp2pgsql