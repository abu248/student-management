# Student Management

A Django application for managing student profiles and course records, with login-protected pages for the dashboard and student directory.

## Run locally

1. Install Python 3.12 or newer.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the project requirements:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create the database and an administrator account:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start the development server and sign in:

   ```powershell
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/> in your browser.

## Configuration

For deployment, set `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS` using environment variables. Do not commit passwords, secret keys, `.env` files, the local SQLite database, or uploaded student photos.

## Deploy to Render

The repository includes a `render.yaml` Blueprint that provisions the Django web service and PostgreSQL database. In Render, choose **New → Blueprint**, connect this GitHub repository, enter your own administrator username, email, and password when prompted, and apply the Blueprint. Render generates the production `SECRET_KEY` and configures the service to accept its assigned hostname. The initial administrator is created on startup only if that username does not already exist; remove the `DJANGO_SUPERUSER_*` values from the Render service after the first successful deploy.

Free Render web services sleep when idle and use temporary local storage. Free Render PostgreSQL databases expire after 30 days. Upgrade the database before that deadline to keep student records. Student photo uploads are stored on the web service's temporary filesystem and do not persist across restarts or deploys; use durable object storage before relying on uploaded photos.

Do not reuse credentials or secret keys from local files.
