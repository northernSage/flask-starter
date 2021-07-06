[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/northernSage/flask-starter/master.svg)](https://results.pre-commit.ci/latest/github/northernSage/flask-starter/master)

# flask Starter App

*A containerized docker scaffold for web applications using Flask.*

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

2. Install pre-commit hooks

    ```pre-commit install```

3. Tweak environment variables using the *.env* files inside *envfiles* directories in each service root (*app* and *worker*)

    **Important:** Do not forget to create and set a new ```SECRET_KEY``` value and set FLASK_ENV to "production" when deploying!

4. Build and start containers in production or development mode

    ```docker-compose -f docker-compose.prod.yml up --build```

    or

    ```docker-compose -f docker-compose.dev.yml up --build```

**Obs.** You can access the application by visiting the URI ```https://<host-machine-ip>``` at first (```https://<host-machine-ip>:5000``` for development mode), and later customize Nginx to your desired url format, hostname, port, etc.

6. Open a command shell in your *web* container and apply migrations

    ```docker-compose -f .\docker-compose.dev/prod.yml exec web bash```

    ```flask db upgrade```

7. Create a test user

    ```flask create-test-user```

7. Set your application repository as new remote so you can push changes to it

    ```git remote set-url origin <your-app-repo-url>```

    ```git push -u origin master```

You are all set, get coding! :)

### Testing

In order to run tests, first open a command shell in the application container

   ```docker-compose -f docker-compose.dev/prod.yml exec web bash```

and execute the test suite

   ```pytest```

**Aditional information:**

```flask create-test-user``` creates user *appuser* of password: *appuser*
