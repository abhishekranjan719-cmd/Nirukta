# Azure VM Deployment Guide

**Created:** 2026-01-03
**Status:** Planning
**Target:** Production deployment on Azure VM with Docker Compose

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [High-Level Deployment Steps](#high-level-deployment-steps)
- [TODO Checklist](#todo-checklist)
- [Nginx Reverse Proxy Configuration](#nginx-reverse-proxy-configuration)
- [Security Hardening](#security-hardening)
- [Monitoring & Maintenance](#monitoring--maintenance)

---

## Overview

### Do You Need a Reverse Proxy? **YES!**

**Why Nginx Reverse Proxy is Essential:**

1. ✅ **SSL/TLS Termination**
   - Single point for HTTPS certificates (Let's Encrypt)
   - No need to configure SSL in each service
   - Automatic certificate renewal

2. ✅ **Domain Routing**
   - `app.yourdomain.com` → Frontend
   - `api.yourdomain.com` → Backend
   - Single VM, multiple domains

3. ✅ **Security**
   - Hide internal ports from public access
   - Rate limiting and DDoS protection
   - Request filtering and validation

4. ✅ **Performance**
   - Static file caching
   - Gzip compression
   - Connection pooling

5. ✅ **Simplified Management**
   - Single entry point (ports 80/443)
   - Easy to add new services
   - Centralized logging

---

## Architecture

### Current Architecture (Docker Compose)
```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Docker Compose Network (Internal)              │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Frontend │  │ Backend  │  │  Engine  │     │
│  │  :5173   │  │  :8000   │  │  :8001   │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Postgres │  │  Redis   │  │ Langfuse │     │
│  │  :5432   │  │  :6379   │  │  :3000   │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│                                                 │
│  ┌──────────┐  ┌──────────┐                    │
│  │ LiteLLM  │  │  MinIO   │                    │
│  │  :4000   │  │  :9000   │                    │
│  └──────────┘  └──────────┘                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Production Architecture (Azure VM + Nginx)
```
                        Internet
                           │
                           │
                    ┌──────▼──────┐
                    │ Azure VM    │
                    │             │
┌───────────────────┼─────────────┼───────────────────┐
│                   │  Nginx      │                   │
│                   │  :80/:443   │                   │
│                   └──────┬──────┘                   │
│                          │                          │
│          ┌───────────────┼───────────────┐         │
│          │               │               │         │
│    ┌─────▼─────┐   ┌────▼────┐   ┌─────▼─────┐  │
│    │ Frontend  │   │ Backend │   │ Langfuse  │  │
│    │ (Nginx)   │   │ :8000   │   │ :3000     │  │
│    │ Static    │   └────┬────┘   └───────────┘  │
│    └───────────┘        │                        │
│                    ┌────▼────┐                    │
│                    │ Engine  │                    │
│                    │ :8001   │                    │
│                    └────┬────┘                    │
│                         │                         │
│    ┌────────────────────┴────────────────────┐  │
│    │   Internal Services (Not Exposed)       │  │
│    │                                          │  │
│    │  Postgres • Redis • LiteLLM • MinIO     │  │
│    │  :5432    • :6379 • :4000   • :9000     │  │
│    │                                          │  │
│    └──────────────────────────────────────────┘  │
│                                                   │
│  Docker Compose Network                          │
└───────────────────────────────────────────────────┘

Exposed Ports:
- 80 (HTTP - redirects to HTTPS)
- 443 (HTTPS - Nginx handles SSL)

Internal Services: All on Docker network, no external exposure
```

---

## Prerequisites

### Azure Resources Needed

1. **Virtual Machine**
   - Size: Standard_D4s_v3 (4 vCPUs, 16 GB RAM) or higher
   - OS: Ubuntu 22.04 LTS
   - Disk: 128 GB Premium SSD minimum
   - Network: Public IP address

2. **Networking**
   - Network Security Group (NSG) with rules for ports 80, 443, 22
   - Public IP address (static preferred)
   - DNS A records configured

3. **Domain Names**
   - Main domain: `yourdomain.com`
   - Subdomain for app: `app.yourdomain.com`
   - Subdomain for API: `api.yourdomain.com`
   - Subdomain for Langfuse: `langfuse.yourdomain.com`

4. **SSL Certificates**
   - Let's Encrypt (free, auto-renewable)
   - Or purchase commercial SSL certificates

---

## High-Level Deployment Steps

### Phase 1: Infrastructure Setup (Azure Portal/CLI)
1. Create Azure VM with Ubuntu 22.04
2. Configure Network Security Group (ports 80, 443, 22)
3. Assign static public IP
4. Configure DNS A records pointing to VM IP
5. SSH into VM and secure it

### Phase 2: VM Preparation
1. Update system packages
2. Install Docker and Docker Compose
3. Install Nginx
4. Install Certbot (Let's Encrypt)
5. Configure firewall (ufw)

### Phase 3: Application Deployment
1. Clone project repository
2. Configure environment variables (.env)
3. Update docker-compose.yml for production
4. Build and start containers
5. Verify internal services are running

### Phase 4: Nginx Reverse Proxy Setup
1. Configure Nginx for each domain
2. Set up SSL certificates with Let's Encrypt
3. Configure automatic certificate renewal
4. Test HTTPS access

### Phase 5: Security Hardening
1. Close unnecessary ports
2. Configure fail2ban
3. Set up Docker logging
4. Enable automatic security updates
5. Configure backup strategy

### Phase 6: Monitoring & Maintenance
1. Set up monitoring (Prometheus/Grafana or Azure Monitor)
2. Configure log aggregation
3. Set up alerting
4. Document maintenance procedures
5. Create backup/restore procedures

---

## TODO Checklist

Copy this checklist and track your progress:

### ☐ Azure Infrastructure Setup

#### ☐ VM Creation
- [ ] Create Azure VM (Ubuntu 22.04, Standard_D4s_v3 or higher)
- [ ] Configure 128GB Premium SSD
- [ ] Assign static public IP address
- [ ] Note VM public IP: `_________________`
- [ ] Create/configure Network Security Group:
  - [ ] Allow port 22 (SSH) from your IP only
  - [ ] Allow port 80 (HTTP) from anywhere
  - [ ] Allow port 443 (HTTPS) from anywhere
  - [ ] DENY all other inbound traffic

#### ☐ DNS Configuration
- [ ] Purchase domain or use existing: `_________________`
- [ ] Create DNS A records:
  - [ ] `app.yourdomain.com` → VM IP
  - [ ] `api.yourdomain.com` → VM IP
  - [ ] `langfuse.yourdomain.com` → VM IP
- [ ] Verify DNS propagation (can take 24-48 hours)
  - [ ] Test: `nslookup app.yourdomain.com`

#### ☐ SSH Access
- [ ] Generate SSH key pair locally: `ssh-keygen -t rsa -b 4096`
- [ ] Add public key to VM during creation OR
- [ ] Copy public key to VM: `ssh-copy-id user@VM_IP`
- [ ] Test SSH connection: `ssh user@VM_IP`
- [ ] Create SSH config entry for easy access

---

### ☐ VM Initial Setup

#### ☐ System Updates
```bash
# Update package lists
sudo apt update

# Upgrade all packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git vim ufw fail2ban

# Reboot if kernel was updated
sudo reboot
```

- [ ] Run system update commands
- [ ] Reboot VM if needed

#### ☐ Docker Installation
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Install Docker Compose V2
sudo apt install -y docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

- [ ] Install Docker
- [ ] Install Docker Compose
- [ ] Add user to docker group
- [ ] Log out and back in (for group to take effect)
- [ ] Verify: `docker ps` works without sudo

#### ☐ Nginx Installation
```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Verify installation
sudo systemctl status nginx
curl http://VM_IP  # Should show Nginx welcome page
```

- [ ] Install Nginx
- [ ] Verify Nginx is running
- [ ] Test access from browser

#### ☐ Certbot Installation (Let's Encrypt)
```bash
# Install Certbot and Nginx plugin
sudo apt install -y certbot python3-certbot-nginx

# Verify installation
certbot --version
```

- [ ] Install Certbot
- [ ] Verify installation

#### ☐ Firewall Configuration
```bash
# Enable UFW
sudo ufw --force enable

# Allow SSH (IMPORTANT - do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status verbose
```

- [ ] Configure UFW firewall
- [ ] Verify ports 22, 80, 443 are open
- [ ] Test SSH still works after enabling firewall

---

### ☐ Application Deployment

#### ☐ Code Deployment
```bash
# Clone repository
cd ~
git clone <your-repo-url> app
cd app

# Create .env file from template
cp .env.example .env

# Edit .env file
vim .env
```

- [ ] Clone project repository to VM
- [ ] Create `.env` file with production values
- [ ] Update all passwords and secrets in `.env`
- [ ] Set `MODE=dev` (production mode)
- [ ] Configure all database passwords
- [ ] Set strong REDIS_PASSWORD
- [ ] Generate Langfuse encryption keys: `openssl rand -hex 32`
- [ ] Update domain names in CORS settings

#### ☐ Docker Compose Modifications
- [ ] Review `docker-compose.yml`
- [ ] Remove port mappings for internal services:
  - [ ] Postgres (5432) - should NOT be exposed
  - [ ] Redis (6379) - should NOT be exposed
  - [ ] LiteLLM internal port (4000) - should NOT be exposed
  - [ ] MinIO (9000/9001) - should NOT be exposed
- [ ] Keep only internal Docker network communication
- [ ] Backend should listen on 8000 (internal only)
- [ ] Langfuse should listen on 3000 (internal only)

#### ☐ Build and Start Services
```bash
# Pull latest images
docker compose pull

# Build custom images
docker compose build

# Start services
docker compose up -d

# Check status
docker compose ps

# Check logs
docker compose logs -f
```

- [ ] Build/pull Docker images
- [ ] Start all services: `docker compose up -d`
- [ ] Verify all containers are running: `docker compose ps`
- [ ] Check logs for errors: `docker compose logs`
- [ ] Wait for all services to be healthy (may take 2-3 minutes)

#### ☐ Verify Internal Services
```bash
# Test backend (from VM)
curl http://localhost:8000/health

# Test Langfuse (from VM)
curl http://localhost:3000

# Check database connections
docker compose exec backend python -c "from app.config import settings; print(settings.postgres.main_database_url)"
```

- [ ] Test backend health endpoint
- [ ] Test Langfuse access
- [ ] Verify database connections
- [ ] Check Redis connection
- [ ] Verify LiteLLM proxy is running

---

### ☐ Nginx Reverse Proxy Configuration

#### ☐ Backend API Configuration
```bash
# Create Nginx config
sudo vim /etc/nginx/sites-available/api.yourdomain.com
```

- [ ] Create Nginx config file (see example below)
- [ ] Enable site: `sudo ln -s /etc/nginx/sites-available/api.yourdomain.com /etc/nginx/sites-enabled/`
- [ ] Test config: `sudo nginx -t`
- [ ] Reload Nginx: `sudo systemctl reload nginx`

#### ☐ Frontend Configuration
```bash
# Create Nginx config
sudo vim /etc/nginx/sites-available/app.yourdomain.com
```

- [ ] Create Nginx config for frontend
- [ ] Build frontend with production env: `VITE_BACKEND_URL=https://api.yourdomain.com npm run build`
- [ ] Copy frontend build to Nginx: `sudo cp -r frontend/dist /var/www/app.yourdomain.com`
- [ ] Enable site and reload Nginx

#### ☐ Langfuse Configuration
```bash
# Create Nginx config
sudo vim /etc/nginx/sites-available/langfuse.yourdomain.com
```

- [ ] Create Nginx config for Langfuse
- [ ] Enable site and reload Nginx

#### ☐ SSL Certificate Setup
```bash
# Obtain SSL certificates for all domains
sudo certbot --nginx -d api.yourdomain.com
sudo certbot --nginx -d app.yourdomain.com
sudo certbot --nginx -d langfuse.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

- [ ] Obtain SSL certificate for API domain
- [ ] Obtain SSL certificate for App domain
- [ ] Obtain SSL certificate for Langfuse domain
- [ ] Verify HTTPS access for all domains
- [ ] Test automatic renewal
- [ ] Certificates will auto-renew via systemd timer

---

### ☐ Security Hardening

#### ☐ Fail2ban Configuration
```bash
# Install fail2ban
sudo apt install -y fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo vim /etc/fail2ban/jail.local

# Enable and start
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

- [ ] Install fail2ban
- [ ] Configure SSH protection
- [ ] Configure Nginx protection
- [ ] Start fail2ban service

#### ☐ SSH Hardening
```bash
# Edit SSH config
sudo vim /etc/ssh/sshd_config
```

- [ ] Disable password authentication (use SSH keys only)
- [ ] Disable root login
- [ ] Change SSH port (optional but recommended)
- [ ] Restart SSH: `sudo systemctl restart sshd`

#### ☐ Environment Variables Security
- [ ] Ensure `.env` file has secure permissions: `chmod 600 .env`
- [ ] Verify no secrets in git: `git status`
- [ ] Confirm `.env` is in `.gitignore`

#### ☐ Docker Security
- [ ] Set up Docker resource limits in docker-compose.yml
- [ ] Configure Docker logging: `sudo vim /etc/docker/daemon.json`
- [ ] Restart Docker: `sudo systemctl restart docker`

---

### ☐ Testing & Validation

#### ☐ Functional Testing
- [ ] Access `https://app.yourdomain.com` in browser
- [ ] Login to application
- [ ] Test backend API: `curl https://api.yourdomain.com/health`
- [ ] Access Langfuse: `https://langfuse.yourdomain.com`
- [ ] Test conversation functionality
- [ ] Verify Langfuse logging is working
- [ ] Test all main features end-to-end

#### ☐ Security Testing
- [ ] Verify HTTP redirects to HTTPS
- [ ] Check SSL certificate is valid (A+ rating on ssllabs.com)
- [ ] Confirm internal ports are not accessible externally:
  ```bash
  # From your local machine (should fail/timeout)
  telnet VM_IP 5432  # Postgres
  telnet VM_IP 6379  # Redis
  telnet VM_IP 8001  # Engine
  ```
- [ ] Verify only ports 22, 80, 443 are open
- [ ] Test fail2ban is working (check logs)

#### ☐ Performance Testing
- [ ] Load test backend API
- [ ] Monitor resource usage: `htop`, `docker stats`
- [ ] Check response times
- [ ] Verify caching is working

---

### ☐ Monitoring & Logging

#### ☐ Application Logs
```bash
# View Docker logs
docker compose logs -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

- [ ] Set up log rotation for Docker
- [ ] Set up log rotation for Nginx
- [ ] Configure centralized logging (optional)

#### ☐ Monitoring Setup (Optional but Recommended)
- [ ] Set up Azure Monitor alerts for VM metrics
- [ ] Configure disk space alerts
- [ ] Set up uptime monitoring (UptimeRobot or similar)
- [ ] Configure email/SMS alerts for downtime

---

### ☐ Backup & Disaster Recovery

#### ☐ Backup Strategy
```bash
# Database backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker compose exec -T postgres pg_dumpall -U postgres > backup_$DATE.sql
```

- [ ] Create database backup script
- [ ] Set up automated daily backups (cron job)
- [ ] Configure backup retention policy
- [ ] Store backups in Azure Blob Storage or separate disk
- [ ] Test restore procedure

#### ☐ Disaster Recovery Plan
- [ ] Document restore procedures
- [ ] Create VM snapshot in Azure
- [ ] Store critical configs in secure location
- [ ] Document emergency contacts and procedures

---

### ☐ Documentation & Handoff

#### ☐ Documentation
- [ ] Document all URLs and credentials (in secure location)
- [ ] Create runbook for common operations
- [ ] Document troubleshooting steps
- [ ] Write deployment notes

#### ☐ Access & Credentials
- [ ] Store all passwords in secure password manager
- [ ] Share access with team (if applicable)
- [ ] Document who has access to what

---

## Nginx Reverse Proxy Configuration

### Backend API Configuration

File: `/etc/nginx/sites-available/api.yourdomain.com`

```nginx
# Backend API - https://api.yourdomain.com
upstream backend {
    server localhost:8000;
    keepalive 32;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name api.yourdomain.com;

    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect all other HTTP traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.yourdomain.com;

    # SSL certificates (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/api.yourdomain.com/chain.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/api.yourdomain.com.access.log;
    error_log /var/log/nginx/api.yourdomain.com.error.log;

    # Max upload size
    client_max_body_size 10M;

    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    # Proxy to backend
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # WebSocket support (if needed)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Disable buffering for streaming responses
        proxy_buffering off;
    }

    # Health check endpoint (optional - no auth required)
    location /health {
        proxy_pass http://backend/health;
        access_log off;
    }
}
```

### Frontend Configuration

File: `/etc/nginx/sites-available/app.yourdomain.com`

```nginx
# Frontend - https://app.yourdomain.com

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name app.yourdomain.com;

    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect all other HTTP traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name app.yourdomain.com;

    # SSL certificates (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/app.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.yourdomain.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/app.yourdomain.com/chain.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/app.yourdomain.com.access.log;
    error_log /var/log/nginx/app.yourdomain.com.error.log;

    # Root directory for static files
    root /var/www/app.yourdomain.com;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA routing - all routes go to index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### Langfuse Configuration

File: `/etc/nginx/sites-available/langfuse.yourdomain.com`

```nginx
# Langfuse - https://langfuse.yourdomain.com
upstream langfuse {
    server localhost:3000;
    keepalive 32;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name langfuse.yourdomain.com;

    # Let's Encrypt challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect all other HTTP traffic to HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name langfuse.yourdomain.com;

    # SSL certificates (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/langfuse.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/langfuse.yourdomain.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/langfuse.yourdomain.com/chain.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/langfuse.yourdomain.com.access.log;
    error_log /var/log/nginx/langfuse.yourdomain.com.error.log;

    # Max upload size
    client_max_body_size 20M;

    # Timeouts (Langfuse can have longer requests)
    proxy_connect_timeout 90s;
    proxy_send_timeout 90s;
    proxy_read_timeout 90s;

    # Proxy to Langfuse
    location / {
        proxy_pass http://langfuse;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # WebSocket support
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Enable Sites

```bash
# Enable all sites
sudo ln -s /etc/nginx/sites-available/api.yourdomain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/app.yourdomain.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/langfuse.yourdomain.com /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Security Hardening

### 1. Fail2ban Configuration

File: `/etc/fail2ban/jail.local`

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
destemail = your-email@example.com
sendername = Fail2Ban
action = %(action_mwl)s

[sshd]
enabled = true
port = 22
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/*error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
port = http,https
logpath = /var/log/nginx/*error.log
```

### 2. SSH Hardening

File: `/etc/ssh/sshd_config`

```bash
# Disable password authentication
PasswordAuthentication no

# Disable root login
PermitRootLogin no

# Use SSH protocol 2 only
Protocol 2

# Limit login attempts
MaxAuthTries 3
MaxSessions 2

# Disconnect idle sessions
ClientAliveInterval 300
ClientAliveCountMax 2
```

### 3. Docker Logging Configuration

File: `/etc/docker/daemon.json`

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### 4. Automated Security Updates

```bash
# Install unattended-upgrades
sudo apt install -y unattended-upgrades

# Enable automatic security updates
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Check service status
docker compose ps

# Check disk space
df -h

# Check memory usage
free -h

# Check Docker logs for errors
docker compose logs --tail=100 | grep -i error

# Check Nginx logs for errors
sudo tail -100 /var/log/nginx/error.log
```

### Weekly Maintenance

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean up Docker
docker system prune -f

# Check SSL certificate expiry
sudo certbot certificates

# Review fail2ban logs
sudo fail2ban-client status sshd
```

### Monthly Tasks

- Review and rotate logs
- Check backup integrity
- Review resource usage trends
- Update documentation
- Security audit

---

## Troubleshooting

### Common Issues

**1. Cannot access application**
```bash
# Check if Nginx is running
sudo systemctl status nginx

# Check if Docker containers are running
docker compose ps

# Check Nginx error logs
sudo tail -50 /var/log/nginx/error.log

# Check Docker logs
docker compose logs backend
```

**2. SSL certificate issues**
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates manually
sudo certbot renew

# Test certificate renewal
sudo certbot renew --dry-run
```

**3. Port conflicts**
```bash
# Check what's using a port
sudo netstat -tulpn | grep :8000

# Check firewall rules
sudo ufw status verbose
```

**4. Database connection issues**
```bash
# Check Postgres is running
docker compose ps postgres

# Check Postgres logs
docker compose logs postgres

# Test connection from backend
docker compose exec backend python -c "from app.config import settings; print(settings.postgres.main_database_url)"
```

---

## Cost Estimation

### Azure VM Costs (Approximate)

- **Standard_D4s_v3** (4 vCPUs, 16 GB RAM): ~$140/month
- **Premium SSD 128GB**: ~$20/month
- **Static Public IP**: ~$4/month
- **Bandwidth** (1TB/month): ~$90/month

**Total estimated cost: ~$250-300/month**

### Cost Optimization Tips

1. Use Azure Reserved Instances (save up to 30%)
2. Configure auto-shutdown during non-business hours
3. Use Azure Cost Management alerts
4. Monitor and optimize storage usage
5. Consider Azure Container Instances for specific services

---

## Next Steps After Deployment

1. **Load Testing**
   - Test application under load
   - Identify bottlenecks
   - Optimize as needed

2. **CI/CD Pipeline**
   - Set up GitHub Actions for automated deployment
   - Configure staging environment
   - Implement blue-green deployment

3. **Advanced Monitoring**
   - Set up Prometheus + Grafana
   - Configure custom dashboards
   - Set up alerting rules

4. **Scaling Strategy**
   - Plan for horizontal scaling
   - Consider Azure Container Instances
   - Evaluate Azure Kubernetes Service (AKS)

5. **Disaster Recovery**
   - Test backup/restore procedures
   - Document recovery time objectives (RTO)
   - Create disaster recovery runbook

---

**Document Owner:** DevOps Team
**Last Reviewed:** 2026-01-03
**Next Review:** 2026-02-03
