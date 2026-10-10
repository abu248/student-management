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
