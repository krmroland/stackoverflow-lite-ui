# Stack overflow lite 

[![Maintainability](https://api.codeclimate.com/v1/badges/a0ff7755b693b7523265/maintainability)](https://codeclimate.com/github/krmroland/stackoverflow-lite-ui/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4f220c8d224a4603adfc367189499c12)](https://www.codacy.com/project/krmroland/stackoverflow-lite-ui/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=krmroland/stackoverflow-lite-ui&amp;utm_campaign=Badge_Grade_Dashboard)
[![BCH compliance](https://bettercodehub.com/edge/badge/krmroland/stackoverflow-lite-ui?branch=master)](https://bettercodehub.com/)

| Service         | Master        | Develop    |
| -------------   |-------------|----------|
|Travis CI status | [![Build Status](https://travis-ci.org/krmroland/stackoverflow-lite-ui.svg?branch=master)](https://travis-ci.org/krmroland/stackoverflow-lite-ui)|[![Build Status](https://travis-ci.org/krmroland/stackoverflow-lite-ui.svg?branch=develop)](https://travis-ci.org/krmroland/stackoverflow-lite-ui)|
|Coveralls|[![Coverage Status](https://coveralls.io/repos/github/krmroland/stackoverflow-lite-ui/badge.svg)](https://coveralls.io/github/krmroland/stackoverflow-lite-ui)|[![Coverage Status](https://coveralls.io/repos/github/krmroland/stackoverflow-lite-ui/badge.svg?branch=e4049139-api)](https://coveralls.io/github/krmroland/stackoverflow-lite-ui?branch=develop)|



StackOverflow-lite-ui  is a platform where people can ask questions and provide answers.
# Getting Started
In your terminal 
1. Clone the repo locally to your machine by running `git clone https://github.com/krmroland/stackoverflow-lite-ui`
2. change your current directory (`cd`) to wherever you cloned the app in 1 above.

#### Demos
This __api__ is currently  has two versions hosted on heroku;
- [v.1.0 (In memory Data Structures)](https://andela-stackoverflow-v1.herokuapp.com/api/v1.0/)
- [V.1.1 (Uses Databases)](https://andela-stackoverflow.herokuapp.com/api/v1.1/)

#### Requirements
- [Python](https://www.python.org/) A general purpose programming language
- [Pip](https://pypi.org/project/pip/) A tool for installing python packages
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)  A tool to create isolated Python environments
- [Postgresql](https://www.postgresql.org/) An open  source relational database

#### Development setup
- Create a virtual environment and activate it
  ```bash
   virtualenv venv
   source /venv/bin/activate
  ```
- Install dependencies 
  ```bash
  pip3 install requirements.txt
  ```
- Setting environmental variables

  Rename `.env.example` to `.env` and replace the dummy values with the actual values e.g the database name for both the testing environment and the development environment.


#### Run the database migrations
```bash
 # Delete all tables and recreate them
 flask migrate:fresh
``` 
#### Run the application
```bash
python run.py
```

#### Running tests
```bash

pytest

#with coverage
pytest pytest   -v --cov api/app
```
#### API REST End Points
| End Point                                           | Verb |Use                                            |
| ----------------------------------------------------|------|-----------------------------------------------|
|`/api/v1.0/`                                         |GET   |API index                                      |
|`/api/v1.0/questions`                                |GET   |Gets a list of Questions                       |
|`/api/v1.0/questions`                                |POST  |Stores a Question resource                     |
|`/api/v1.0/questions/<int:id>`                       |GET   |Gets a Question resource of a given ID         |
|`/api/v1.0/questions/<int:id> `                      |PATCH |Updates a Question resource                    |
|`/api/v1.0/questions<int:id>`                        |DELETE|Deletes a Question resource                    |
|`/api/v1.0/questions/<int:id>/answers`               |GET   |Gets a answers of a specific question          |
|`/api/v1.0/questions/<int:id>/answers`               |POST  |Adds a an answer to a question                 |
|`/api/v1.0/questions/<int:id>/answers/<int:id>`      |GET   |Gets a specific answer                         |
|`/api/v1.0/questions/<int:id>/answers/<int:id>`      |UPDATE|Updates an existing answer                     |
|`/api/v1.0/questions/<int:id>/answers/<int:id>`      |DELETE|Deletes an existing answer                     |
|`/api/v1.0/auth/signup`                              |POST  | Creates a user account                        |
|`/api/v1.0/auth/login`                               |POST  |Exchanges  user credentials with a token       |


#### Built With
- [Flask](http://flask.pocoo.org/) A microframework for Python based on Werkzeug, Jinja 2 


## Acknowledgments
 A Special thanks goes to 
1. [Andela](https://andela.com/) for having given me an opportunity to participate in the boot camp, without them , this application wouldn't be a success.

2. [UI Faces](https://uifaces.co/) for providing free avatar sources that I used in the UI templates .
