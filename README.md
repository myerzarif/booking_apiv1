# Booking Platform API VERSION 1

## INSTALL Requirements and start app without docker (docker instructions are listed at the next section and its recommended to use docker to run the project)
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- cp .env.sample .env (edit .env file)
- python manage.py runserver
- make sure you installed and configured redis, postgres and nginx on your server

--------------------------

## StartApp by Docker
- sudo docker network create booking_apiv1_network 
- sudo docker volume create --name=booking_apiv1_psql
- cp .env.sample .env (edit .env file)
- sudo docker-compose up -d
- sudo docker exec -it booking_apiv1 python manage.py collectstatic
- Now you should be able to see the doc page: http://localhost:5000/help-swagger

To reset the app:
- sudo docker-compose down; sudo docker-compose up -d
- docker compose down; docker compose up -d
--------------------------

## Testing
- python manage.py test

--------------------------

## Coverage Test
- coverage run --source='.' manage.py test
- coverage report

--------------------------

### Migrate app
- sudo docker exec booking_apiv1 python manage.py makemigrations
- sudo docker exec booking_apiv1 python manage.py makemigrations account # Migrate specific app
- sudo docker exec booking_apiv1 python manage.py migrate

--------------------------

### Run Shell and exec command with ipython in django shell
- sudo docker exec -it booking_apiv1 python manage.py shell -i ipython

--------------------------

### Build Application
- sudo docker compose build booking_apiv1
- sudo docker compose up -d 

--------------------------

### Restart Application 
- sudo docker-compose restart booking_apiv1

--------------------------

### Test Application 
- sudo docker exec -it booking_apiv1 python manage.py test
- sudo docker exec -it booking_apiv1 python manage.py test account  # Test Specific App
- sudo docker exec -it booking_apiv1 python manage.py test account -k 2 # Test Specific App and search in test name

--------------------------

### Coverage Application in Testing
- sudo docker exec -it booking_apiv1 coverage run --source='.' manage.py test
- sudo docker exec -it booking_apiv1 coverage report

--------------------------

## Show log On Command Line
- sudo docker-compose logs --tail 50 booking_apiv1

--------------------------

## Run CELERY for common app
- python -m celery -A common worker
- docker exec -it booking_apiv1 celery -A common.celery worker -l info

--------------------------

## CREATE SUPERUSER (Active user with TECH role)
- python manage.py createsuperuser
- docker exec -it booking_apiv1 python manage.py createsuperuser

--------------------------

## db
psql postgresql://bookingusr:R016eJ9Gej7@localhost:5434/bookingdb