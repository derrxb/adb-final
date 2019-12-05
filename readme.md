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

##### Step 1: Create Python virtual environment

```
virtualenv venv
```

#### Step 2: Install project dependencies
```
pip install -r requirements.txt
```

##### Step 3: Create Neo4j graph database
* Set the username as `neo4j` and password as `password`
* Start graph server

##### Step 4: Seed the database with the project data
* This is a work in progress. We're still figuring it out.

##### Step 3: Start Flask server
* To start the Flask app, run the command below:

```
FLASK_APP=runserver.py flask run
```

Not sure why but for some reason `python runserver.py` fails to launch the app. So if you can't get the app to run
it might be because you are running this command. (I tried like a billion times).