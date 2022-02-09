# Fluxis

## Getting Started
Install python and npm

Install the necessary packages for the backend:
`pip install -r packages/fluxis_api/requirements.txt`

Install the necessary packages for the frontend:
`npm install --prefix packages/fluxis_frontend`

Setup the database
`python packages/fluxis_api/manage.py migrate`

Now to run the server, simply:
Start the backend
`python packages/fluxis_api/manage.py runserver`

Start the frontend (in a separate terminal from the backend)
`npm start --prefix packages/fluxis_frontend`