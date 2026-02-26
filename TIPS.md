## Pydantic validation

https://www.reddit.com/r/Python/comments/1odk7pl/comment/nkuwjcm/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button


## Running FastAPI and React app in separate containers

https://vardhmanandroid2015.medium.com/beginners-guide-for-containerizing-application-deploying-a-full-stack-fastapi-and-react-app-001f2cac08a8

- Use nginx as a reverse proxy to direct all requests to /api
- Difference/caveat: prefix all FastAPI routes with "/api" for it to work; example doesn't do this I believe, but another example on GitHub does this


## Run shp2pgsql commands in PostGIS containers

`docker exec -it db shp2pgsql --help` =>
`Error loading shared library libintl.so.8: No such file or directory (needed by /usr/local/bin/shp2pgsql)`
when using `postgis/postgis:18-3.6-alpine`

https://github.com/litsynp/postgis-import-shp-example?tab=readme-ov-file
directs us to this issue
https://gis.stackexchange.com/questions/384381/shp2pgsql-available-in-postgis13-3-1-alpine-but-no-in-postgis13-3-1-docker-ima
