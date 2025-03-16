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
- **Database**: PostgreSQL
- **Web Server**: Nginx
- **Deployment**: Docker, Docker Compose
- **Host**: Digital Ocean Droplet

## Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/gheidorn/ortbo.git
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

## Docker Setup (Local Development)

1. Clone the repository:
   ```
   git clone https://github.com/gheidorn/ortbo.git
   cd ortbo
   ```

2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file and update the settings.

4. Build and start the containers:
   ```
   docker compose up -d --build
   ```

5. Create a superuser:
   ```
   docker compose exec web python manage.py createsuperuser
   ```

6. Access the application at http://localhost:80

## Deployment to Digital Ocean

### Prerequisites

- Docker and Docker Compose installed on your Digital Ocean Droplet
- Domain name configured to point to your Droplet's IP address
- Basic knowledge of Nginx and SSL configuration

### Deployment Steps

1. Clone the repository on your Digital Ocean Droplet:
   ```
   git clone https://github.com/gheidorn/ortbo.git
   cd ortbo
   ```

2. Create a `.env` file with your production settings:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file with appropriate values:
   ```
   # Generate a secure random key
   SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
   
   # Set to False in production
   DEBUG=False
   
   # Update with your domain
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DOMAIN=yourdomain.com
   
   # Set secure database credentials
   POSTGRES_DB=ortbo
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_secure_password
   DATABASE_URL=postgres://your_db_user:your_secure_password@db:5432/ortbo
   ```

4. Configure SSL:
   ```
   # Generate self-signed certificates for development
   # For production, use Let's Encrypt or other certificate authority
   mkdir -p nginx/ssl
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/ssl/key.pem -out nginx/ssl/cert.pem
   ```

5. Build and start the containers:
   ```
   docker compose up -d --build
   ```

6. Monitor the logs to ensure everything is working:
   ```
   docker compose logs -f
   ```

7. Access your application at https://yourdomain.com

### Production Considerations

1. For proper SSL certificates, consider using Let's Encrypt with Certbot:
   ```
   # Install Certbot
   apt-get update
   apt-get install certbot python3-certbot-nginx
   
   # Obtain certificates
   certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

2. Set up regular database backups:
   ```
   # Add to crontab for daily backups
   0 0 * * * docker compose exec -T db pg_dump -U your_db_user ortbo > /path/to/backups/ortbo_$(date +\%Y\%m\%d).sql
   ```

3. Configure firewall rules to only allow traffic on necessary ports (22, 80, 443).

4. Set up monitoring and alerting with tools like Datadog or Prometheus.

## License

This project is licensed under the MIT License - see the LICENSE file for details.