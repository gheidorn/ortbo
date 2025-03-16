#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting deployment process for Ortbo..."

# Check if running as root
if [ "$(id -u)" != "0" ]; then
   echo "⚠️  This script must be run as root or with sudo" 1>&2
   exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your production settings before continuing!"
    exit 1
fi

# Install Docker and Docker Compose if not already installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io
fi

if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    apt-get install -y docker-compose-plugin
fi

# Setup SSL directory
mkdir -p nginx/ssl

# Check if SSL certificates exist, otherwise generate self-signed ones
if [ ! -f nginx/ssl/cert.pem ] || [ ! -f nginx/ssl/key.pem ]; then
    echo "🔐 Generating self-signed SSL certificates..."
    # Get domain from .env file
    DOMAIN=$(grep DOMAIN .env | cut -d '=' -f2)
    
    # If domain is not set, use a placeholder
    if [ -z "$DOMAIN" ]; then
        DOMAIN="ortbo.example.com"
    fi
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/key.pem \
        -out nginx/ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
    
    echo "⚠️  Using self-signed certificates. For production, consider using Let's Encrypt."
fi

# Pull latest code if in git repository
if [ -d .git ]; then
    echo "📥 Pulling latest code..."
    git pull
fi

# Build and start the containers
echo "🏗️  Building and starting containers..."
docker compose down
docker compose up -d --build

# Wait for the web service to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Apply migrations
echo "🔄 Applying database migrations..."
docker compose exec web python manage.py migrate

# Create backup directory
mkdir -p backups

# Create a backup script
echo "📝 Creating backup script..."
cat > backup.sh << 'EOL'
#!/bin/bash
BACKUP_DIR="$(pwd)/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/ortbo_$TIMESTAMP.sql"

# Get database credentials from .env
source .env

# Create backup
echo "Creating database backup: $BACKUP_FILE"
docker compose exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > "$BACKUP_FILE"

# Keep only the last 7 backups
echo "Cleaning up old backups..."
ls -t $BACKUP_DIR/*.sql | tail -n +8 | xargs -r rm

echo "Backup completed!"
EOL

chmod +x backup.sh

# Add backup to crontab
echo "📅 Setting up daily backups..."
(crontab -l 2>/dev/null || echo "") | grep -v "backup.sh" > temp_cron
echo "0 0 * * * $(pwd)/backup.sh >> $(pwd)/backups/backup.log 2>&1" >> temp_cron
crontab temp_cron
rm temp_cron

# Set up firewall
echo "🔒 Configuring firewall..."
apt-get install -y ufw
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable

echo "✅ Deployment completed! Your Ortbo application should be running at https://your-domain"
echo "   Check the logs with: docker compose logs -f"
echo "   Create a superuser with: docker compose exec web python manage.py createsuperuser"