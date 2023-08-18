# Weather collector [pet project]

## Features
The application consists of 3 modules:
1. Fetching world's largest cities from third-party API.
2. Fetching weather for provided cities from third-party API and store data into database.
3. Preparation of a temperature report for each city in the form of a graph.



## Built With
![](https://img.shields.io/badge/python-3.11-purple)
![](https://img.shields.io/badge/SQL_Alchemy-2.0.18-purple)
![](https://img.shields.io/badge/alembic-1.11.1-purple)
![](https://img.shields.io/badge/asyncpg-0.28.0-purple)
![](https://img.shields.io/badge/pydantic-1.10.10-purple)
![](https://img.shields.io/badge/aiohttp-3.8.4-purple)
![](https://img.shields.io/badge/flet-0.8.2-purple)
![](https://img.shields.io/badge/matplotlib-3.7.2-purple)


## Getting Started
### Setup
1. Clone the repo.
    ```sh
    git clone https://github.com/baltikaa9/weather_collector.git
    ```
2. Define environment variables
    ```sh
   cd weather_collector
   nano .env
    ```
   
   ```env
    OXILOR_API_KEY=<your_api_key>
    OPENWEATHER_API_KEY=<your_api_key>
    DB_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/weather_collector
    ```
   
Getting API keys:
- [OXILOR_API_KEY](https://data.oxilor.ru/0/api-keys)
- [OPENWEATHER_API_KEY](https://home.openweathermap.org/api_keys)



### Run docker compose
- For windows
  - Up container: `docker-compose -f docker-compose.yml up --build`
  - Up container in detach mode: `docker-compose -f docker-compose.yml up --build -d`
  - Down container: `docker-compose -f docker-compose.yml down && docker network prune --force`

- For linux
  - Up container: `make up`
  - Up container in detach mode: `make up-d`
  - Down container: `make down`

> WARNING! <br>
> If database connection fails, try again in a few seconds. It could be because postgres server is not running yet.
 
Visualization of collected data is available in the browser at http://localhost:8550


### Run as python script
1. Activate virtual environment.
   ```bat
   python -m venv venv
   venv\Sripts\activate

2. Install requirements.
    ```bat
   pip install -r requirements.txt
   ```

3. Migrate database.
    ```bat
   alembic upgrade head
   ```
4. Run 

`python main.py init` - Fetch information about cities.
> WARNING! <br>
> When starting this module, all stored weather information will be lost.
    
 `python main.py collect` - Every hour fetch weather information for each city.

 `python main.py visual` - Visualization of collected data.

 `python main.py visual -w` - Visualization of collected data in [browser](http://localhost:8550).
   
## Database connection
- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Password: `postgres`
- Database: `weather_collector`
