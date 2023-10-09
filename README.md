# Tasks management app

This app aims to make it easy to manage the daily tasks.

# Development

The development environment is provided by a Docker setup in the folder `docker`. It provides:

- A MySQL database
- A python image with Poetry

To run the setup, a `.env` file is required which contains

```
MYSQL_PASSWORD=<password for the MySQL database>
DB_DATA_DIR=<local directory where to store the database data>
BACKEND_DIR=<local directory with the backend code>
```
