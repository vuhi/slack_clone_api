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
    - DB_PASSWORD=
    - PUBLIC_KEY=
    - PRIVATE_KEY=
    - IS_DEV=
    - GG_OAUTH_CLIENT_ID=
    - GG_OAUTH_CLIENT_SECRET=
    - FB_OAUTH_CLIENT_ID=
    - FB_OAUTH_CLIENT_SECRET=
  ...
  environment:
    - POSTGRES_DB=
    - POSTGRES_USER=
    - POSTGRES_PASSWORD=
  ...
  ```
  or create `.env` file at root folder: 
  ```
  DB_NAME=your_db_name
  DB_USER=your_db_user_name
  DB_PASSWORD=your_db_pass_word
  PRIVATE_KEY=your_rsa_private_key
  PUBLIC_KEY=your_rsa_public_key
  IS_DEV=your_is_dev
  GG_OAUTH_CLIENT_ID=your_google_oauth_client_id
  GG_OAUTH_CLIENT_SECRET=your_google_oauth_client_secret
  FB_OAUTH_CLIENT_ID=your_facebook_oauth_client_id
  FB_OAUTH_CLIENT_SECRET=your_facebook_oauth_client_secret
  ```
+ Generate RSA key: https://travistidwell.com/jsencrypt/demo/
+ Run: `docker-compose up`
+ Run in background: `docker-compose up -d`
+ To stop the app: `docker-compose down`
+ To run cmd with docker: 
  + bash into docker: `docker exec -it backend bash` & run your cmd. Run `exit` to exit the current bash
  + or run: `docker-compose run backend sh -c "your cmd here"`


### Helpful:
+ Starts the Python interactive interpreter: `django-admin shell`
+ If you install a new dependency:
  + Stop containers with: `docker-compose down`
  + If you cannot stop container, get container id: `docker ps -a`, force delete with: `docker rm -f container-id`
  + Install dependencies with `pip`  
  + Run this cmd at root folder after install any new dependencies: `pip freeze > requirements.txt`
  + Run containers: `docker-compose up`
+ If you create a new model, remember to migrate with: `python manage.py makemigrations` then `python manage.py migrate`
+ If you want to restart the database entirely new, remove the docker volume on database container:
  + get volume name: `docker volume ls`
  + remove volume: `docker volume rm volume_name`
+ webhook: https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
+ Oauth configuration:
  + Google: https://console.cloud.google.com/apis/dashboard
  + FB: https://developers.facebook.com/apps

