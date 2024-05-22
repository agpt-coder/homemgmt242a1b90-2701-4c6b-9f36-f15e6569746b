---
date: 2024-05-21T20:16:53.172668
author: AutoGPT <info@agpt.co>
---

# homemgmt

use `pip install HomeAssistant-API` to expose the api endpoints to list the services, the entities, and rooms

**Features**

- **Service Listing** Provides a clear and easily navigable list of all available services within the Home Assistant environment. Users can install the necessary API via `pip install HomeAssistant-API`.

- **Entity Overview** Displays a comprehensive list of all entities controlled by Home Assistant, including installation via `pip install HomeAssistant-API`.

- **Room Management** Allows users to view and manage entities grouped by rooms, enabling more intuitive control over different areas of their home. Includes `pip install HomeAssistant-API` installation instruction.


## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'homemgmt'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
