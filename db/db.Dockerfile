FROM postgis/postgis:17-master AS builder
RUN apt update
RUN apt install -y postgis
RUN which shp2pgsql


FROM postgis/postgis:17-master

COPY --from=builder /usr/bin/shp2pgsql /usr/bin/shp2pgsql

# install unzip for Debian-based container image
RUN apt-get update && apt-get install -y unzip

# the following happens during build time (image build). where we are the "root" user, therefore the files inside of
# /tmp/data are owned by root. During run time, the container runs as the "postgres" user, which doesn't have write
# permission to the directory owned by root.
COPY migrations/ /docker-entrypoint-initdb.d/
COPY data/ /tmp/data/

RUN chmod +x /docker-entrypoint-initdb.d/*.sh
RUN chown -R postgres:postgres /tmp/data/

# check shp2pgsql is installed
RUN shp2pgsql