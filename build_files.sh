echo "Installing Packages"
python3 -m pip install -r requirements.txt

echo "Generating Translation Files"
django-admin makemessages -a  

echo "Compiling Translations"
django-admin compilemessages  

echo "Migrating DB"
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collecting static files"
python3 manage.py collectstatic --noinput

