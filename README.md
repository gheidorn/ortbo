# Ortbo - Engineering Team Management

Ortbo is a Django web application for visualizing engineer skills and organizing engineering teams. It provides a sophisticated interface for tracking engineer skill profiles and enables team leaders to organize engineers into balanced teams.

## Features

- **Engineer Skill Visualization**: View engineer skills using radar charts and detailed breakdowns
- **Team Organization**: Drag-and-drop interface for organizing engineers into teams
- **Team Skill Analysis**: Aggregate and visualize team skill distributions
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Django 5.0+
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Heroku-ready

## Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ortbo.git
   cd ortbo
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Load example data:
   ```
   python add_example_data.py
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://localhost:8000/fivetool/

## Deployment to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Manual Deployment Steps

1. Create a Heroku app:
   ```
   heroku create your-app-name
   ```

2. Add PostgreSQL add-on:
   ```
   heroku addons:create heroku-postgresql:hobby-dev
   ```

3. Configure environment variables:
   ```
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. Deploy your code:
   ```
   git push heroku main
   ```

5. Run migrations:
   ```
   heroku run python manage.py migrate
   ```

6. Load example data:
   ```
   heroku run python add_example_data.py
   ```

7. Create a superuser:
   ```
   heroku run python manage.py createsuperuser
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.