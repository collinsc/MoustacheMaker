npm run build
pipenv shell
$env:FLASK_APP="runserver.py"
$env:FLASK_ENV="development"
python -m flask run  --no-reload

exit