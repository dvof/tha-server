To run server_sqlite.py:

`cd server`

`sudo gunicorn --bind 0.0.0.0:5000 --workers 4 'server_sqlite:app' --env DEBUG=true`

or:

`sudo gunicorn --bind 0.0.0.0:5000 --workers 4 'server_sqlite:app'`

Admin rights (sudo) is needed for writing at `/mnt/databases`. Storage directory is hardcoded at the moment.

Add service script to run in background and at boot:

```
sudo cp systemd/tha_server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tha_server.service
sudo systemctl start tha_server.service
```

