import os

os.environ['FLASK_APP'] = 'recommender.py'
os.environ['FLASK_ENV'] = 'development'

os.system("flask run")
