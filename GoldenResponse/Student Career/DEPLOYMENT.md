# Deployment Guide - Student Career Portal

This guide provides detailed instructions for deploying the Student Career & Placement Portal to production.

## Pre-deployment Checklist

- [ ] Update `SECRET_KEY` in settings.py to a strong random value
- [ ] Set `DEBUG = False` in production settings
- [ ] Configure `ALLOWED_HOSTS` with your domain names
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure database (PostgreSQL recommended for production)
- [ ] Set up email backend for notifications
- [ ] Configure static files and media storage
- [ ] Set up backup strategy for database
- [ ] Test all functionality before deployment
- [ ] Set up monitoring and logging

## Option 1: Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git installed

### Steps

1. **Create Heroku app**:
```bash
heroku login
heroku create your-app-name
```

2. **Create Procfile**:
```
web: gunicorn career_portal.wsgi
worker: python manage.py celery worker -l info
release: python manage.py migrate
```

3. **Create runtime.txt**:
```
python-3.11.0
```

4. **Add Buildpacks**:
```bash
heroku buildpacks:add heroku/python
```

5. **Set environment variables**:
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY='your-strong-secret-key'
heroku config:set ALLOWED_HOSTS='your-app.herokuapp.com'
```

6. **Push to Heroku**:
```bash
git push heroku main
```

7. **Create superuser**:
```bash
heroku run python manage.py createsuperuser
```

## Option 2: Deploy to DigitalOcean

### Prerequisites
- DigitalOcean account
- SSH access to your droplet
- Domain name

### Steps

1. **Create Droplet**:
   - Select Ubuntu 20.04 LTS
   - Choose appropriate size (2GB RAM minimum)
   - Add SSH key for access

2. **Connect to Droplet**:
```bash
ssh root@your_server_ip
```

3. **Update System**:
```bash
apt update
apt upgrade -y
```

4. **Install Dependencies**:
```bash
apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx gunicorn supervisor
```

5. **Clone Repository**:
```bash
git clone https://github.com/your-repo/careerhub.git
cd careerhub
```

6. **Create Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

7. **Configure PostgreSQL**:
```bash
sudo -u postgres psql

CREATE DATABASE careerhub;
CREATE USER careerhub_user WITH PASSWORD 'strong_password';
ALTER ROLE careerhub_user SET client_encoding TO 'utf8';
ALTER ROLE careerhub_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE careerhub_user SET default_transaction_deferrable TO on;
ALTER ROLE careerhub_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE careerhub TO careerhub_user;
\q
```

8. **Configure Django Settings** (Create production settings):
```python
# careerhub/settings_prod.py
from .settings import *

DEBUG = False
SECRET_KEY = 'your-strong-secret-key'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'careerhub',
        'USER': 'careerhub_user',
        'PASSWORD': 'strong_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

9. **Run Migrations**:
```bash
python manage.py migrate --settings=career_portal.settings_prod
python manage.py collectstatic --noinput --settings=career_portal.settings_prod
```

10. **Configure Gunicorn** (create `/etc/systemd/system/gunicorn.service`):
```ini
[Unit]
Description=gunicorn daemon for careerhub
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/careerhub
ExecStart=/path/to/careerhub/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/run/gunicorn.sock \
    career_portal.wsgi:application

[Install]
WantedBy=multi-user.target
```

11. **Configure Nginx** (create `/etc/nginx/sites-available/careerhub`):
```nginx
upstream careerhub {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 20M;
    
    location /static/ {
        alias /path/to/careerhub/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/careerhub/media/;
    }
    
    location / {
        proxy_pass http://careerhub;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

12. **Enable Nginx Site**:
```bash
ln -s /etc/nginx/sites-available/careerhub /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

13. **Set up SSL with Let's Encrypt**:
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

14. **Enable Services**:
```bash
systemctl enable gunicorn
systemctl start gunicorn
systemctl enable nginx
```

## Option 3: Deploy to AWS EC2

### Prerequisites
- AWS Account
- EC2 instance running Ubuntu 20.04
- Elastic IP assigned
- Security group configured

### Steps (Similar to DigitalOcean with AWS-specific modifications)

1. Connect to EC2 instance via SSH
2. Follow steps 3-14 from DigitalOcean guide above
3. Use AWS RDS for database instead of local PostgreSQL
4. Use AWS S3 for media/static files storage
5. Configure AWS CloudFront for CDN

## Post-Deployment Steps

### 1. Set up Monitoring

```bash
pip install django-debug-toolbar
pip install sentry-sdk
```

### 2. Configure Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/careerhub/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 3. Set up Backup Strategy

```bash
# Backup database daily
0 2 * * * pg_dump -U careerhub_user careerhub > /backup/careerhub_$(date +\%Y\%m\%d).sql

# Backup media files weekly
0 3 * * 0 tar -czf /backup/media_$(date +\%Y\%m\%d).tar.gz /path/to/careerhub/media/
```

### 4. Configure Email

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@careerhub.edu'
```

### 5. Set up Automated Updates

```bash
# Install unattended-upgrades for security updates
apt install unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

## Troubleshooting

### Static Files Not Loading
- Run: `python manage.py collectstatic --clear --noinput`
- Check Nginx configuration for correct paths
- Verify file permissions: `chmod -R 755 staticfiles/`

### Database Connection Issues
- Check PostgreSQL is running: `systemctl status postgresql`
- Verify database credentials in settings
- Check firewall rules: `ufw allow 5432`

### Gunicorn Not Starting
- Check syntax: `gunicorn --check-config career_portal.wsgi:application`
- Check logs: `journalctl -u gunicorn -n 100`
- Verify Python environment is activated

### SSL Certificate Issues
- Renew certificate: `certbot renew`
- Set up auto-renewal: `systemctl enable certbot.timer`

## Scaling Considerations

### Load Balancing
- Use Nginx as reverse proxy
- Deploy multiple Gunicorn workers
- Consider HAProxy for advanced load balancing

### Caching
- Configure Redis for session storage
- Use Memcached for application caching
- Implement CDN for static assets

### Database Optimization
- Add database indexes
- Use connection pooling (pgBouncer)
- Implement read replicas
- Regular VACUUM and ANALYZE

### Monitoring
- Set up Prometheus for metrics
- Use Grafana for visualization
- Configure alerts for critical metrics
- Monitor disk space and resource usage

## Security Hardening

1. **Firewall Configuration**:
```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

2. **Fail2Ban Installation**:
```bash
apt install fail2ban
systemctl enable fail2ban
```

3. **Regular Security Updates**:
```bash
apt update && apt upgrade -y
```

4. **Disable Root SSH**:
```bash
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart sshd
```

## Maintenance Tasks

### Daily
- Monitor logs for errors
- Check system resources
- Monitor application health

### Weekly
- Backup database
- Backup media files
- Review security logs

### Monthly
- Update dependencies
- Review performance metrics
- Update SSL certificates (if needed)
- Test disaster recovery

## Support and Documentation

For more information:
- Django Documentation: https://docs.djangoproject.com/
- Nginx Documentation: https://nginx.org/en/docs/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Let's Encrypt: https://letsencrypt.org/

---

**Last Updated**: May 2026
