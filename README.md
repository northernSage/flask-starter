# flask Starter App

*A docker-containerized scaffold for web applications using Flask.*

### Docker services

- web (wsgi app and gunicorn)
- nginx (pre-configured, https-ready reverse proxy to gunicorn)
- redis (in-memory task broker for background jobs or cache)
- worker (isolated container for background tasks)

### Features

- secure forms (flask-wtf)
- Database ORM (flask-sqlalchemy)
- Database migrations (flask-migration)
- Login, Logout, Register, password recovery (flask-login)
- Error logging (email logs with flask-mail and rotating files)
- Test suite (pytest)

Pre-configuration for Let's encrypt SSL/TLS certificate (Grade A on SSL labs)

### How to Set Up

1. Clone this repository

    ```git clone https://github.com/northernSage/flask-starter.git```

2. Create a virtual environment and activate it

    Windows:
    ```py -m venv venv; .\venv\Scripts\Activate```

    Linux:
   ```python3 -m venv venv && source venv/bin/activate```

2. Install dependencies

    ```pip install -r requirements.txt```

3. Set environment variables using the *.env* files inside *envfiles* directories in each service root (*app* and *worker*)
    
    **Important:** Do not forget to create and set a new ```SECRET_KEY``` value and set FLASK_ENV to "production" when deploying!

3. Start up docker services in production or development mode, respectively, running

    ```docker-compose -f docker-compose.dev.yml up --build```

    or

    ```docker-compose -f docker-compose.prod.yml up --build```

**Obs.** You can access the application by visiting the URI ```https://<host-machine-ip>``` at first, and later customize Nginx to your desired url format, hostname, port, etc.

5. Open a command shell in your *web* container and initialize the database

    ```docker-compose -f .\docker-compose.dev/prod.yml exec web bash```

    and run

    ```flask init-db```

6. Create the test/development user

    ```flask create-test-user```

7. Create initial migration

    ```flask db migrate -m "first migration"```

8. Apply migrations 

    ```flask db upgrade```

9. Set your application repository as new remote so you can push changes to it 

	```git remote set-url origin <your-app-repo-url>```

    ```git push -u origin master```

You are all set, get codding! :)

### Testing

In order to run tests, first open a command shell in your application container

    ```docker-compose -f docker-compose.dev/prod.yml exec web bash```

and execute the test suite 

    ```pytest```

**Aditional information:**

```flask create-test-user``` creates user *appuser* of password: *appuser*
