## RUN UP PROJECT
+ Clone project from github: `git clone https://github.com/vuhi/slack_clone_api.git`
+ `cd` into your project location
### - Local:
+ Set up your virtual environment:  
    + `py -m venv venv`
    + `venv\Scripts\active` (Window) or `source venv/bin/activate` (Mac)
+ Install dependencies: `pip install -r requirements.txt`
+ Download & install PostgresSQL: https://www.postgresql.org/download/
+ Adjust `DATABASE` in `api_core/settings.py` with your postgres setting:
  ```
  DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'backend_db',
        'USER': ...,
        'PASSWORD': ...,
        'HOST': 'localhost',
        'PORT': 5432,
      }
  }
  ```
+ Migrate your schema: `python manage.py migrate`
+ Run server: `python manage.py runserver`

### - Dockerize:
+ Download & Install Docker: https://docs.docker.com/get-docker/
+ Run docker desktop app
+ Check if:
  + docker is running: `docker --version` 
  + docker-compose is running: `docker-compose --version`
  + if not, install docker-compose: https://docs.docker.com/compose/install/
+ Fill configuration in `docker-compose.yml`:
  ```
  ...
  environment:
    - DB_NAME=
    - DB_USER=
    - DB_PASS=
  ...
  environment:
    - POSTGRES_DB=
    - POSTGRES_USER=
    - POSTGRES_PASSWORD=
  ...
  ```
  or using create `.env` file at root folder: 
  ```
  DB_NAME=your_db_name
  DB_USER=your_db_user_name
  DB_PASSWORD=your_db_pass_word
  ```
+ Run: `docker-compose up`
+ Run in background: `docker-compose up -d`
+ To stop the app: `docker-compose down`
+ To run cmd with docker: 
  + bash into docker: `docker exec -it backend bash` & run your cmd. Run `exit` to exit the current bash
  + or run: `docker-compose run backend sh -c "your cmd here"`
