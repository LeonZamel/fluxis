# Fluxis

## Getting Started
0. Install python and npm 
1. Clone this repository and `cd` into it

2. Install the necessary packages for the backend:\
`pip install -r api/requirements.txt`

3. Install the necessary packages for the frontend:\
`npm install --prefix frontend`

4. Setup the database\
`python api/manage.py migrate`

5. Now to run the server, simply:
    - Start the backend\
`python api/manage.py runserver`

    - Start the frontend (in a separate terminal from the backend)\
`npm start --prefix frontend`