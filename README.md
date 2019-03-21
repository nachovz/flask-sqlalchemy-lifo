# Persistant data

Flask offers a nice ecosystem of modules that we can use to expand the functionalities of our API's, one of those is flask-SQLAlchemy, which is a layer between the endpoints and the database, specifically SQLite (similar to MySQL, both use SQL).

## Configuration of the database
  
Before *using* a database we must go through a configuration check list:
1. Install *flask-SQLAlchemy*: ```sudo pip install Flask-SQLAlchemy```
2. Install *flask-migrate*: ```sudo pip install flask-migrate```
  
*flask-migrate* will help us handling the changes and different versions regarding the SQLite database. This [article](https://flywaydb.org/getstarted/why) makes a good point why we need to use migrations. More on *how* to do migrations after a couple steps.

3. Now we need to configure our flask app. Add these lines into your ```app.py``` (or main file):
  
*app.py*
```python
import os
import sqlalchemy
...
from flask_migrate import Migrate
  
app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change_this_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)
  
...

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```

You'll get an error "undefined variable db", that's because ```db``` (which represents our **d**ata**b**ase object variable) needs to be initialized, we'll move the database logic to another file ([logic decouple](https://www.techopedia.com/definition/16907/decoupled-architecture)) ```models.py```. 

We will define our models in this file. The models represent the entities of our application which hold the data we want to persist.
  
*models.py*
```python
from flask_sqlalchemy import SQLAlchemy
  
db = SQLAlchemy()
  
#Example model Item 
#It represents an Item in a list
#you can use any name, first letter in CAPS
  
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return 'Item: %s (%s)' % (self.text, self.created_on)
```

Then update *app.py*:
  
*app.py*
```python
import os
import sqlalchemy
...
from flask_migrate import Migrate
#Importing db and model(s)
from models import db, Item
  
app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change_this_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)
  
...
  

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```

4. After your *app.py* **and** *models.py* files are set:
    + Run ```flask db init``` to initialize the config files (migrations) for the DB.
    + Run ```flask db migrate``` to run the migrations.
    + Run ```flask db upgrade``` update SQLite.
  
The last 2 steps **must** be executed after avery change done to the class models. This is to update the database with the new structure (it may produce data loss).
  
**Configuration done!**

## Using the models
  
Now to get the information from the database we must use the *query* method from the model

```python
items = Item.query.all()
# All Item persisted in the database 

```
  
You can check the other functions in the flask_sqlalchemy [documentation](http://flask-sqlalchemy.pocoo.org/2.3/queries/)

### Example

If you need to list all the *Item* instances from the database you can update your *app.py* to:
*app.py*
```python
import os
import sqlalchemy
...
from flask_migrate import Migrate
#Importing db and model(s)
from models import db, Item
  
app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change_this_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)
  
  
  
@app.route('/')
def list():
    items = Item.query.all()
    response = []
    for i in items:
        response.append("%s" % i)
    
    return jsonify(response)



app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```
  
