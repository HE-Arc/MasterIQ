# MasterIQ

Step to follow to run the project:

1. Clone the repository
2. Go to the folder api
    ```bash
    cd api
    ```
3. install the python environment with pipenv, and then run it
    ```bash
    pipenv install
    pipenv shell
    ```
3. Run the migrations
    ```bash
    python manage.py migrate
    ```
4. Create your superuser
    ```bash
    python manage.py createsuperuser --email admin@example.com --username admin
    ```
5. Run the backend server
    ```bash
    python manage.py runserver
    ```
6. Go in the folder frontend
    ```bash
    cd ../frontend
    ```
7. install the node environment with npm, and then run it
    ```bash
    npm install
    ```
7. Run the frontend server
    ```bash
    npm run dev
    ```


note for the frontend guys : Quasar is not installed yet, so I'll let you decide wether to use it or not :)