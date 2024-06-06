echo "BUILD START"
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo "BUIKD END"