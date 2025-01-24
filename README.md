To run server_sqlite.py:

`sudo gunicorn --bind 0.0.0.0:5000 --workers 4 'server_sqlite:app' --reload --env DEBUG=true`

or:

`sudo gunicorn --bind 0.0.0.0:5000 --workers 4 'server_sqlite:app'`

Admin rights (sudo) is needed for writing at `/mnt/databases`. Storage directory is hardcoded at the moment.
