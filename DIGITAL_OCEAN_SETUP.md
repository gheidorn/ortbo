# Digital Ocean Deployment Guide for Ortbo

This guide will walk you through setting up a Digital Ocean droplet and deploying the Ortbo application.

## 1. Create a Digital Ocean Droplet

1. Sign up for Digital Ocean if you haven't already: https://www.digitalocean.com/
2. Create a new Droplet with the following specifications:
   - **Distribution**: Ubuntu 22.04 LTS
   - **Plan**: Basic (Shared CPU)
   - **Size**: 2GB RAM / 1 CPU (Recommended minimum)
   - **Region**: Choose one close to your primary users
   - **Authentication**: SSH keys (recommended) or Password
   - **Hostname**: ortbo-production (or your preference)

## 2. Configure DNS

1. If you already have a domain, point it to your Digital Ocean Droplet's IP address by creating these DNS records:
   - Type: A, Name: @ (or your subdomain), Value: Your Droplet's IP address
   - Type: A, Name: www, Value: Your Droplet's IP address

2. Alternatively, you can use Digital Ocean's domain services:
   - In the Digital Ocean control panel, go to "Networking" -> "Domains"
   - Add your domain and create the necessary A records

## 3. Initial Server Setup

1. SSH into your Droplet:
   ```
   ssh root@your-droplet-ip
   ```

2. Update packages:
   ```
   apt update && apt upgrade -y
   ```

3. Create a non-root user:
   ```
   adduser ortbo
   usermod -aG sudo ortbo
   ```

4. Set up SSH keys for the new user:
   ```
   mkdir -p /home/ortbo/.ssh
   cp ~/.ssh/authorized_keys /home/ortbo/.ssh/
   chown -R ortbo:ortbo /home/ortbo/.ssh
   chmod 700 /home/ortbo/.ssh
   chmod 600 /home/ortbo/.ssh/authorized_keys
   ```

5. Install Git:
   ```
   apt install git -y
   ```

## 4. Deploy Ortbo

1. Switch to the 'ortbo' user:
   ```
   su - ortbo
   ```

2. Clone the repository:
   ```
   git clone https://github.com/gheidorn/ortbo.git
   cd ortbo
   ```

3. Run the deployment script:
   ```
   sudo ./deploy.sh
   ```

4. When prompted, edit the `.env` file with your production settings:
   ```
   nano .env
   ```
   
   Make sure to set:
   - `SECRET_KEY` (a secure random string)
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (your domain names)
   - `DOMAIN` (your primary domain)
   - Secure database credentials

5. Run the deployment script again:
   ```
   sudo ./deploy.sh
   ```

6. Create an admin user:
   ```
   sudo docker compose exec web python manage.py createsuperuser
   ```

7. Your site should now be accessible at your domain!

## 5. Set Up Let's Encrypt SSL (Optional but Recommended)

For proper SSL certificates (instead of self-signed):

1. Install Certbot:
   ```
   sudo apt update
   sudo apt install certbot python3-certbot-nginx
   ```

2. Stop the Nginx container:
   ```
   sudo docker compose stop nginx
   ```

3. Obtain SSL certificates:
   ```
   sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
   ```

4. Copy the certificates to the Nginx SSL directory:
   ```
   sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /home/ortbo/ortbo/nginx/ssl/cert.pem
   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /home/ortbo/ortbo/nginx/ssl/key.pem
   ```

5. Start the Nginx container:
   ```
   sudo docker compose start nginx
   ```

6. Set up auto-renewal:
   ```
   sudo crontab -e
   ```
   
   Add this line:
   ```
   0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /home/ortbo/ortbo/nginx/ssl/cert.pem && cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /home/ortbo/ortbo/nginx/ssl/key.pem && docker restart ortbo_nginx_1
   ```

## 6. Monitoring and Maintenance

1. Check container status:
   ```
   sudo docker compose ps
   ```

2. View logs:
   ```
   sudo docker compose logs
   ```

3. Follow logs in real-time:
   ```
   sudo docker compose logs -f
   ```

4. Restart all services:
   ```
   sudo docker compose restart
   ```

5. Update the application:
   ```
   cd /home/ortbo/ortbo
   git pull
   sudo docker compose up -d --build
   ```

## 7. Backup and Restore

The deployment script sets up automatic daily backups to the `backups` directory.

To manually create a backup:
```
./backup.sh
```

To restore a backup:
```
sudo docker compose exec -T db pg_restore -U ortbo_user -d ortbo < backups/your-backup-file.sql
```

## Troubleshooting

1. **Cannot connect to the website**:
   - Check if containers are running: `sudo docker compose ps`
   - Check firewall settings: `sudo ufw status`
   - Check Nginx logs: `sudo docker compose logs nginx`

2. **Database errors**:
   - Check database logs: `sudo docker compose logs db`
   - Ensure database credentials in `.env` match those in `docker-compose.yml`

3. **Application errors**:
   - Check web application logs: `sudo docker compose logs web`
   - Connect to web container: `sudo docker compose exec web bash`