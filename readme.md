## Project overview

A MOOCs social network (not really sure if this is what we're doing) built
with Flask.

## Requirements

* Python >= 3.7
* Neo4j graph database
* Flask
* Python virtural env
  * ```pip install virtualenv```

## Installation

##### Step 1: Create Python virtual environment or activate virual environment
* If this is the first time you are running the project, create the python virtual environment with the command below:

```
virtualenv venv
```

* However if you've already ran the project before, activate the virtual env with this command:
```
source venv/bin/activate
```
* If Windows:
```
venv\bin\activate
```

#### Step 2: Install project dependencies
```
pip install -r requirements.txt
```

##### Step 3: Create Neo4j graph database
* Set the username as `neo4j` and password as `password`
* Start graph server

##### Step 4: Seed the database with the project data
* To seed the database run the following command (Ensure you are in the top directory):
```
python scripts/seed.py
```

##### Step 3: Start Flask server
* To start the Flask app, run the command found below:

```
FLASK_DEBUG=1 FLASK_APP=api/runserver.py FLASK_ENV=development flask run
```
* If Windows:
```
SET FLASK_DEBUG=1 FLASK_APP=api/runserver.py SET FLASK_ENV=development flask run
```

Not sure why but for some reason `python runserver.py` fails to launch the app. So if you can't get the app to run
it might be because you are running this command. (I tried like a billion times).