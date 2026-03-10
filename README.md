# Health Outcomes and Social Determinants

### Which Mississippi census tracts exhibit the greatest structural vulnerability to missed or delayed healthcare based on social determinants of health and associated community health outcomes?

Missed or delayed healthcare appointments create both clinical risks for patients and huge financial losses 
($150 billion annually, nationwide) for healthcare providers. Identifying communities structurally vulnerable to missed 
care can help health systems anticipate where appointment gaps and associated revenue losses are most likely to occur.

## Datasets used

- CDC PLACES, Census Tract, 2025 Release: https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Census-Tract-D/cwsq-ngmh/about_data
- 2025 TIGER/Line® Shapefiles: Census Tracts: https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2025&layergroup=Census+Tracts
- American Community Survey 5-Year Data (2009-2024): https://www.census.gov/data/developers/data-sets/acs-5year.html
  - B08201: Household Size by Vehicles Available https://api.census.gov/data/2024/acs/acs5/groups/B08201.html
  - B28002: Presence and Types of Internet Subscriptions in Household https://api.census.gov/data/2024/acs/acs5/groups/B28002.html
  - B17001: Poverty Status in the Past 12 Months https://api.census.gov/data/2024/acs/acs5/groups/B17001.html
  - S2701: Health Insurance Coverage Characteristics https://api.census.gov/data/2024/acs/acs5/subject/groups/S2701.html

## Run this application with docker

`SOCRATA_APP_TOKEN` and `CENSUS_API_KEY` are still required, to be declared in `/api/.env` in the same manner as `/api/.env.example`.

https://evergreen.data.socrata.com/signup

https://api.census.gov/data/key_signup.html

Clone the repository. Make sure you have docker installed locally. Then, from the repository root run the command:
```shell
docker compose up -d
```

Once all containers are created: head to: `http://localhost:3010`

## Run this application locally for development

Clone the repository. Make sure you have python 3.14 and node 24 installed locally (`.python-version`, `.node-version`). There are a number of ways to do this,
the most widely recommended methods being `pyenv` and `nvm` (node version manager), respectively.

##### Set up supporting services and other requirements

Since we are interacting with a relational database we need a PostgreSQL instance running and for that install Docker with `brew install docker` in the terminal, if you are on macOS. There are alternatives such as installing Postgres natively, using SQLite for dev environment, using a managed Postgres instance provisioned by AWS, Azure, Neon, etc., but Docker streamlines things for local development as well as gives us flexibility to mock and test production environments. After that run `docker -v` in the terminal to confirm the installation. Because many of the images seemingly do not ship with the shp2pgsql tool which we will need later, after some experimentation with different images from Docker hub, we use a slightly customized image. Run the following commands.
From the repository root, `cd` into the `db` directory, where the `db.Dockerfile` lies, then run the following commands:
```shell
cd db &&
docker build --platform linux/amd64 -f db.Dockerfile -t trubridge-postgis:latest . &&
docker run -d \
  --restart always \
  --platform linux/amd64 \
  --name trubridge-ms-outcomes-db-dev \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=trubridge-ms-outcomes-db-dev \
  -p 5429:5432 \
  trubridge-postgis:latest
```

From the repository root, change directories into the Api with the following command: `cd api`. If you are in the `db` directory from the step before, run `cd ..` then `cd api`.

Inside `api`, take a look at the `.env.example` for all the environment variables needed to run the application as intended. Create a `.env` file in the current directory. Copy and paste everything in `.env.example` into `.env`. For the host:container port mappings, i.e. `5429:5432` from the docker command above, you can change 5429 to anything that isn't already in use in your local system, but just be sure to change the port in the connection string in `.env` as `DB_CONNECTION_STRING=postgresql://postgres:postgres@localhost:<YOUR-PORT>/trubridge-ms-outcomes-db-dev` to match it.

Sign up for access to a Data and Insights open data domain and obtain a Socrata App Token so we can authenticate and make requests for data to Tyler Data and Insights. It's possible to query without an app token but there are rate limits, and eventually we want to maximize access for production environments.
`https://support.socrata.com/hc/en-us/articles/115004055807-How-to-Sign-Up-for-a-Tyler-Data-Insights-ID`
`https://evergreen.data.socrata.com`

Once you do that, click on your profile in the top right corner, and head to Developer Settings, and create an App Token. Copy it to the `.env`, specifically `SOCRATA_APP_TOKEN=`.

##### Run the backend Api

Making sure you are still in the `api` directory in the terminal, create a virtual environment and install the necessary python dependencies with the following commands: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`.

Now run `uvicorn main:app --reload` to start the dev server. After application startup is complete (you may or may not have to wait for a bit for the database to seed), head to `http://127.0.0.1:8000/api` or `http://localhost:8000/api` to make sure you get the proper response.

##### Run the frontend app

To run the React server, open a new terminal window from the project root and change directories into the web app with the command `cd web`. Run `npm install` to install necessary dependencies, and a `node_modules` folder should pop up with everything inside. Then run
`npm run dev` and head to `http://localhost:5173/`.
