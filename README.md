# Hardware Checkout

This is the WMACM hardware checkout system

Built with [Flask](http://flask.pocoo.org/),
[SQLAlchemy](https://docs.sqlalchemy.org/en/13/),
[Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/),
[Flask-Dance](https://flask-dance.readthedocs.io/en/latest/),
and [Flask-Login](https://flask-login.readthedocs.io/en/latest/)

## Enviornment Variables

A number of environment variables are required to run this application:

### `DATABASE_URL`
The URL of the database we should connect to. See the
[SQLAlchemy Docs on Database URLs](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls)

Defaults to `sqlite:///test.db` for testing purposes. Should use a real DB
in production.


### `SECRET_KEY`
A long random string of bytes used for securing session cookies.
See the Flask documentation on [sessions](http://flask.pocoo.org/docs/1.0/quickstart/#sessions)
and [SECRET\_KEY](http://flask.pocoo.org/docs/1.0/config/#SECRET_KEY)

### `BASEURL`
The directory under which all pages are hosted. If you want to host
this application at the root directory, you should leave this variable unset.
E.g. if you wanted
to run this on `example.com/hardware` you would set `BASEURL` to `/hardware`
(Beginning slash IS REQUIRED).

### `ENFORCE_HTTPS`
If set, the application forcibly redirects all insecure
connections to `https://`

### `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`
Values obtained from Google through the Credentials tab in the
[Google API Console](https://console.developers.google.com/)

You'll want an `OAuth 2.0 Client ID`.

The application type is `Web application`.

Google will require a domain name to call back to, so you'll
either need your own or you can test on Heroku
(Just please don't test in production!)

The `Authorized JavaScript origins` should just be that location, and
the `Authorized redirect URIs` should just be:
```
https://YOURDOMAINNAMEHERE/login/google/authorized
```
(https is preferrable and required for real deployment but not for testing)

## How to run

You'll need Python 3 and all the requirements as denoted above, and more
specifically in `requirements.txt`. If you have the `venv` module installed,
you can run `setup.sh` which will install all the requirements to a
virtual environment in the `venv` folder in the current directory.
You can then use `run.sh`, along with a `.env` file to set environment
variables (see above) to run the application.

## Modules

This application is divided into a series of files that each handles a separate
part.

### `main.py`
The application itself. Runs everything. Contains all the setup code
and the routes

### `sql.py`
Handles SQL stuff, like the creation of a session and of the tables.
Only import once so that only one session exists.

Initialized with `auth` and `google` so that `oauthdb` can be set up.

### `models.py`
Contains the model objects for all the tables. See
[SQLalchemy docs on its declarative system](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html)

### `forms.py`
Contains all the `FlaskForm` classes used by `main.py`

### `auth.py`
Contains the functions and objects to manage logins and when they are
required. Also contains an email regex checker because I didn't know where else
to put it and this is the smallest module.

Initialized with flask app, the string name of where it should redirect to
when login is required (See [Login Manager docs]()), and `sql`

### `google.py`
Contains the setup for Flask Dance Google OAuth

### `oauthdb.py`
Contains the setup for storing Flask Dance logins in SQLAlchemy

### `prefix.py`
Handles `BASEURL` (see enviornment variables section)


### `static/style.css`
The stylesheet used to space out a few elements.

Most styling is done by the CSS file of
[our main website](https://github.com/ACMWM/acmwm.github.io)

### `templates/`
Contains all the templates, in
[Jinja2 format](http://jinja.pocoo.org/)


## Database

We create four tables:

### `HW`
Database of hardware objects

### `Users`
Names and emails of authorized users

### `Checkouts`
Contains information on every checkout ever done

See `models.py` for more details on the above three tables

### `flask_dance_oauth`
Table used by Flask-Dance to store OAuth2 tokens
See [it's documentation](https://flask-dance.readthedocs.io/en/latest/storages.html#sqlalchemy)

See `oauthdb.py` for more details on the above table.

## Scripts

`adduser.py <username>`

Adds `username@auth.domain` (currently `username@email.wm.edu`, see `auth.py`)
to the users database


`addhw.py <name> [quantity] [category]`

Adds hardware to the database. `quantity` and `category` are optional
and will be set to `1` and `None` respectively if not passed.
