# OPEN - Educational networking web site for research purposes

## Installation instructions

- **Note:** this project uses python 2.7
- Checkout/clone/download this repository and access its directory
- I recommend using _pyenv_ to manage python versions and _virtual env_ to manage pip packages
  - To create a new _virtual environment_: `virtualenv .` (it will be created in the current directory)
  - To activate the _virtual environemnt_: `source bin/activate`
  
- Update the database username to your username or other of your choice in the `settings.py` file:

```python
DATABASES = {
  ...
  'USER': 'your username'
  ...
}
```

- Create a database called OPENdatabase: `createdb OPENdatabase`
- Install packages from requirements.txt: `pip install -r requirements.txt`
- For the first run, use the following commands:

```shell
./manage.py syncdb
./manage.py migrate
```

- To start the server, use either of these commands:

```shell
./manage.py runserver localhost:8000
gunicorn OPEN.wsgi --log-file -
```

- To access it, go to `localhost:8000` and to access the admin section, go to `localhost:8000/admin`

## Current issues

- Upload function isn't working because it uses Amazon S3 as storage and it isn't working right now
- That also means that forums aren't working
