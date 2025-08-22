

# Docker Compose Setup for Local Development

This Docker Compose configuration sets up a local environment for running the Django application. It builds the app from a `Dockerfile` in the project root, mounts the current directory as a volume for live code changes, exposes the app on port 8001, and sets environment variables for debugging.

## Prerequisites
- Install Docker: Download from [docker.com](https://www.docker.com/products/docker-desktop) and ensure it's running.
- Install Docker Compose: It's included with Docker Desktop, or install separately via `pip install docker-compose` (v1) or use the standalone binary for v2+.
- Ensure you have a `Dockerfile` in the project root (e.g., for building a Python/Django image with dependencies).

## Starting the Application Locally
Follow these steps in your terminal from the project directory (where `docker-compose.yml` is located):

1. **Build and Start the Services**:
   ```
   docker compose build
   ```
   - `--build` ensures the image is rebuilt if changes are made to the Dockerfile or code.
   - This starts the `web` service, running the Django app (assumed to use `manage.py runserver` or similar in the Dockerfile).

2. **Access the App**:
   - Open a browser and go to `http://localhost:8001` (maps to container's port 8000).
   - If your Django app uses a different internal port, adjust the `ports` in `docker-compose.yml`.


3. **Stop the Services**:
   - Press `Ctrl+C` in the terminal, or run `docker-compose down` to stop and remove containers (add `-v` to remove volumes if needed).

## Notes
- **Environment Variables**: `DEBUG=True` enables Django debug mode; `PYTHONUNBUFFERED=1` ensures real-time logging.
- **Volume Mounting**: Changes to code in your local directory will reflect in the container without rebuilding (hot-reloading may require app-specific setup).
- **Troubleshooting**: If ports conflict, change `8001:8000` in the file. Ensure no other services use port 8001. For errors, check Docker logs or verify the Dockerfile installs requirements correctly.
- **Production**: This is for local dev; for prod, use a production server like Gunicorn and secure configurations.

Run `docker-compose --help` for more commands.





# Django Subscription API

This project is a Django REST Framework (DRF) API for managing users, features, plans, and subscriptions in a subscription-based system (e.g., trading plans). It includes user registration/login with JWT authentication, CRUD operations for features/plans/subscriptions, and optimized queries for nested data.

## Features
- User registration and JWT-based authentication.
- Create/retrieve features.
- Create/retrieve/update plans with nested features.
- Create/retrieve/update subscriptions with nested plan details.
- Error handling with standard HTTP status codes.
- Query optimization using `select_related` and `prefetch_related`.

## Prerequisites
- Python 3.8+
- Django 4.0+ and Django REST Framework.
- Dependencies: `djangorestframework`, `djangorestframework-simplejwt`.
- Database: SQLite for development; PostgreSQL recommended for production.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd django-subscription-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

6. Run the server:
   ```
   python manage.py runserver
   ```

## Configuration
- **Settings**: Update `settings.py` with database config, JWT settings (e.g., add SimpleJWT to `REST_FRAMEWORK`), and middleware.
- **URLs**: Include the provided `urlpatterns` in your app's `urls.py`, prefixed with `/api/`.
- **Environment**: Use `.env` for secrets like `SECRET_KEY`.

## API Documentation
All endpoints are prefixed with `/api/`. Use JWT tokens from `/login/` for authenticated requests (add `Authorization: Bearer <access_token>` header). Test with Postman or curl.

### 1. User Registration
- **URL**: `/register/`
- **Method**: POST
- **Permissions**: AllowAny
- **Description**: Creates a new user.
- **Request Body**:
  ```
  {
      "username": "string (required)",
      "email": "email (required)",
      "password": "string (required, write-only)"
  }
  ```
- **Success**: 201 - `{"message": "User registered successfully"}`
- **Error**: 400 - Validation errors.

### 2. User Login
- **URL**: `/login/`
- **Method**: POST
- **Permissions**: AllowAny
- **Description**: Returns JWT tokens.
- **Request Body**:
  ```
  {
      "username": "string (required)",
      "password": "string (required, write-only)"
  }
  ```
- **Success**: 200 - `{"refresh": "token", "access": "token"}`
- **Error**: 401 - `{"error": "Authentication failed"}` or 400.

### 3. Features
- **URL**: `/features/`
- **Methods**: POST (create), GET (list all).
- **POST Body**: Feature fields (e.g., `{"name": "string"}`).
- **Success**: POST 201 - `{"message": "Feature created successfully"}`; GET 200 - Array of features.
- **Error**: 400 - Validation errors.

### 4. Plans
- **URL**: `/plans/`
- **Methods**: POST (create), GET (list with features).
- **POST Body**:
  ```
  {
      "name": "string",
      "price": "decimal",
      "features": [1,/ Feature IDs
  }
  ```
- **Success**: POST 201 - `{"message": "Plan created successfully"}`; GET 200 - Plans with nested features.
- **Error**: 400.

### 5. Update Plan
- **URL**: `/plans/<int:id>/`
- **Method**: PUT (partial update).
- **Body**: Partial fields (e.g., `{"price": 19.99}`).
- **Success**: 200 - `{"message": "Plan updated successfully"}`
- **Error**: 404 - `{"error": "Plan not found"}` or 400.

### 6. Subscriptions
- **URL**: `/subscription/`
- **Methods**: POST (create), GET (list with plans).
- **POST Body**:
  ```
  {
      "plan": 1,
      "start_date": "YYYY-MM-DDTHH:MM:SSZ",
      "is_active": true,
      "user": 1
  }
  ```
- **Success**: POST 201 - `{"message": "Subscription created successfully"}`; GET 200 - Subscriptions with nested plans.
- **Error**: 400.

### 7. Update/Retrieve Subscription
- **URL**: `/subscription/<int:id>/`
- **Methods**: PUT (update), GET (get active by ID).
- **PUT Body**: Partial (e.g., `{"is_active": false}`).
- **Success**: PUT 200 - `{"message": "Subscription updated successfully"}`; GET 200 - Subscription object.
- **Error**: 404 - Not found; 400 - Invalid data.

## Contributing
- Fork, branch, and PR. Add tests with pytest.

## License
MIT License.
