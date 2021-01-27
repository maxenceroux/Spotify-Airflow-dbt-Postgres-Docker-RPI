
# Introduction 

This solution provides a all-in-one service that gathers your Spotify history on a regular basis and pushes it into a PostgreSQL database. For the sake of the technical exercise, I've decided to use FastAPI web framework to expose core endpoints. The workflow is orchestrated by Airflow and dbt helps transforming data into valuable insights (WIP). Every service in containeurized in a docker container. All containers can be launched from a single docker-compose command. 

And ported to Raspbian ARM Architecture
## Spotify 
Sorry Spotify, but since you don't allow users to programaticaly fetch their listens' history, I've implemented a Selenium scrapper to grab a token from your Console. 

# Run 
## Clone repo
```bash
git clone https://github.com/maxenceroux/Spotify-Airflow-dbt-Postgres-Docker.git
```

## Run Docker-Compose
```bash
docker-compose up --build
```
## Migrate with alembic
```bash 
docker-compose run web alembic revision --autogenerate -m "First migration"
docker-compose run web alembic upgrade head
```
## Credentials
If you haven't done it yet, you should first head to https://developer.spotify.com/dashboard/login and create an app. 
Once that app is created, you'll be given a client id and a client secret. 

Add your credentials to the following files :  
- .env 
    - SPOTIPY_CLIENT_ID : client id as created above
    - SPOTIPY_CLIENT_SECRET : client secret as created above
    - SPOTIFY_USER : your Spotify email address (needed for web scrapping)
    - SPOTIFY_PWD : your Spotify password (needed for web scrapping)
    
- services/web/.env
    - SPOTIPY_CLIENT_ID : client id as created above
    - SPOTIPY_CLIENT_SECRET : client secret as created above
    - SPOTIFY_USER : your Spotify email address (needed for web scrapping)
    - SPOTIFY_PWD : your Spotify password (needed for web scrapping)
- docker-compose.yml (under airflow environment variables )
    - MY_USERNAME : random username that will be used to authorize your API calls
    - MY_PASSWORD : random password that will be used to authorize your API calls

# Usage

## FastAPI
1. Head to [localhost:1337/docs](localhost:1337/docs) once the containers are running. 
2. Add your first user using /user endpoint and the aforementioned MY_USERNAME and MY_PASSWORD environment variables you set. 

## PGAdmin
1. Head to [localhost:5050](localhost:5050)
2. Login with email *pgadmin4@pgadmin.org* and password *admin* if unchanged
3. Create a server
    1. Choose a server name
    2. Under connection add *db* as Host name
    3. *5432* as Port
    4. *test_db* as Maintenance database
    5. *postgres* as Username
    6. *postgres* as Password

If data schemes migrations went alright, you can now navigate to the server hierarchy you've just created. Under Databases - postgres - Schemas - public - Tables, you should see 3 tables which correspond to the data model used : 
 - alembic_version
 - song
 - user

## Airflow
1. Head to [localhost:7777](localhost:7777)
2. Make sure that spotify connection is created under Admin - Connections

4 DAGs are imported. 
Core DAGs are *get_spotify_songs* and *most_listened*. 
### Get Spotify Songs
This DAG is the core of the solution. Only 2 tasks : 
1. Get a token from your FastAPI web app
2. Call Spotify API and push results to DB. 

If the dag is off, put in on and it should start fetch your music history. 
Head to PGAdmin and query song table to assert that songs are indeed inserted to the table. It is scheduled to be triggered every 20 minutes. You can easily change this CRON value as you please in /services/airflow/airflow/dags/http_dag.py

### Most Listened
Once songs are added to the table, you could launch *most_listened* DAG. 
Turn it on and trigger the DAG. 
Once completed, head back to PGAdmin, you should now see a new schema under your postgres DB called *test* (Note to myself to change name). *daily_most_listened* table is created with your top 5 most listened artists. Once again name is misleading as it is not trigger daily (but it could be!). 