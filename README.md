## ShortStoryMaker

#### Prerequisits:
Python tested on Python 3.6.8 64bit or 3.7.3 64bit
```
pip install flask
pip install flask-sqlalchemy
pip install flask-login
pip install flask-wtf
```


#### set the FLASK_APP and FLASK_DEBUG values and run it !!outside of "project" Folder!!
```
export FLASK_APP=project
export FLASK_DEBUG=1
flask run
```

##### or in the case of Windoof:
```
set FLASK_APP=project
set FLASK_DEBUG=1
flask run
```

#### Create DB (if not pulled from GIT):
- open Terminal and go on top of project Folder
- make sure the right Python environment is running.
- go into Python REPL and type:
```python
from project import db, create_app
db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.
```
--> db.sqlite should appear in project directory

#### Notes:
If you wish to have more functionality from the beginning, you may want to consider using either the Flask-User or Flask-Security libraries, which are both build on top of the Flask-Login library.
https://scotch.io/tutorials/authentication-and-authorization-with-flask-login#comments

Styling of Flask Forms:
https://stackoverflow.com/questions/34738331/using-flask-wtforms-how-do-i-style-my-form-section-of-the-html
