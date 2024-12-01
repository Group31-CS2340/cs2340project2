echo "Installing Packages"
python3 -m pip install -r requirements.txt
FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

echo "Migrating DB"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files"
python3 manage.py collectstatic --noinput