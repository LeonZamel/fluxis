# Fluxis

## Getting Started
0. Install python and npm 
1. Clone this repository and `cd` into it

2. Install the necessary packages for the backend:\
`pip install -r packages/fluxis_api/requirements.txt`

3. Install the necessary packages for the frontend:\
`npm install --prefix packages/fluxis_frontend`

4. Setup the database\
`python packages/fluxis_api/manage.py migrate`

5. Now to run the server, simply:
    - Start the backend\
`python packages/fluxis_api/manage.py runserver`

    - Start the frontend (in a separate terminal from the backend)\
`npm start --prefix packages/fluxis_frontend`