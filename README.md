# DATACOM NOKIA UPDATER

This app is used for update firmware on Nokia ONTs provisioned on DATACOM OLTs.
The app foresee that the firmware file is alread on OLT with file name ALC.bin.

## Putting in production

The app use gunicorn to run Flask. Use Dockerfile to containerize the app.

There are some optional environment variables:

* ISP = ISP Name
* DB_URL = Database URL if not used default db.sqlite3
* SECRET = Secret used for OLT credentials encryption