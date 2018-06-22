# ConTTudOwebProject

[![Build Status](https://travis-ci.org/ConTTudOweb/ConTTudOwebProject.svg?branch=master)](https://travis-ci.org/ConTTudOweb/ConTTudOwebProject)
[![Code Health](https://landscape.io/github/ConTTudOweb/ConTTudOwebProject/master/landscape.svg?style=flat)](https://landscape.io/github/ConTTudOweb/ConTTudOwebProject/master)
[![Coverage Status](https://coveralls.io/repos/github/ConTTudOweb/ConTTudOwebProject/badge.svg?branch=master)](https://coveralls.io/github/ConTTudOweb/ConTTudOwebProject?branch=master)


## How to develop?

1. Clone the repository;
2. Create a virtualenv with Python 3.5;
3. Activate virtualenv;
4. Install the dependencies;
5. Configure the instance with .env;
6. Run the tests;

```console
git clone https://github.com/ConTTudOweb/ConTTudOwebProject.git
cd ConTTudOwebProject
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```
