# Zuna - Azure VM Deployment Guide

## Table of Contents
1. [Resource Requirements](#resource-requirements)
2. [VM Recommendations](#vm-recommendations)
3. [VM Creation Checklist](#vm-creation-checklist)
4. [Network Security (NSG)](#network-security-nsg)
5. [Reverse Proxy Setup](#reverse-proxy-setup)
6. [Domain & SSL Setup](#domain--ssl-setup)
7. [Cloud-Init Script](#cloud-init-script)
8. [Post-Creation Setup](#post-creation-setup)
9. [Cost Summary](#cost-summary)
10. [Security Checklist](#security-checklist)
11. [Spot VM & Auto-Shutdown](#spot-vm--auto-shutdown)
12. [CI/CD with GitHub Actions](#cicd-with-github-actions)

---

## Resource Requirements

Based on the docker-compose services:

| Service             | Memory            |
|---------------------|-------------------|
| MSSQL Server        | 2 GB (configured) |
| Redis Stack         | 1 GB (configured) |
| ClickHouse          | ~1 GB             |
| PostgreSQL          | ~512 MB           |
| LiteLLM (4 workers) | ~1 GB             |
| Langfuse Web        | ~512 MB           |
| Langfuse Worker     | ~256 MB           |
| MinIO               | ~256 MB           |
| Backend + Engine    | ~512 MB           |
| Frontend + SQLPad   | ~256 MB           |
| **Total**           | **~8-10 GB**      |

---

## VM Recommendations

| Option      | VM Size          | vCPU | RAM   | Monthly Cost* | Use Case              |
|-------------|------------------|------|-------|---------------|-----------------------|
| Budget      | Standard_B4ms    | 4    | 16 GB | ~$120         | Dev/test, light usage |
| Minimum     | Standard_D4s_v5  | 4    | 16 GB | ~$140         | Dev/test              |
| **Recommended** | **Standard_D4as_v5** | **4** | **16 GB** | **~$125** | **AMD-based, good value** |
| Comfortable | Standard_D8as_v5 | 8    | 32 GB | ~$250         | Production            |

*Pay-as-you-go pricing, East US region

### Recommendation

**Standard_D4as_v5** (4 vCPU, 16 GB RAM, ~$125/month)
- AMD EPYC processor, best price/performance ratio
- 16 GB is workable with configured memory limits
- Add 64-128 GB Premium SSD for data

### Cost Saving Tips
- **Reserved Instance (1-year):** Save ~35% → ~$80/month
- **Spot VM (dev only):** Save ~70% → ~$40/month (can be evicted)
- **B-series burstable:** Good if usage is intermittent

---

## VM Creation Checklist

### 1. Basic Configuration

| Setting        | Recommendation                                            |
|----------------|-----------------------------------------------------------|
| Region         | Same as your Azure OpenAI resource (e.g., Southeast Asia) |
| Image          | Ubuntu Server 24.04 LTS (or 22.04 LTS)                    |
| Size           | Standard_D4as_v5 (4 vCPU, 16 GB)                          |
| Authentication | SSH public key (more secure than password)                |
| Username       | Your choice (e.g., `azureuser`)                           |

### 2. Disk Configuration

| Disk      | Size   | Type              | Purpose                   |
|-----------|--------|-------------------|---------------------------|
| OS Disk   | 64 GB  | Premium SSD (P6)  | OS + Docker               |
| Data Disk | 128 GB | Premium SSD (P10) | Docker volumes, databases |

> **Important:** Mount data disk to `/var/lib/docker` for persistent data.

### 3. Azure Portal Steps

```
1. Basics
   ├── Subscription: Your subscription
   ├── Resource Group: Create new "zuna-rg"
   ├── VM Name: zuna-vm
   ├── Region: Southeast Asia (match OpenAI)
   ├── Image: Ubuntu Server 24.04 LTS
   ├── Size: Standard_D4as_v5
   ├── Authentication: SSH public key
   └── Username: azureuser

2. Disks
   ├── OS Disk: Premium SSD, 64 GB
   └── Add Data Disk: Premium SSD, 128 GB

3. Networking
   ├── Virtual Network: Create new or use existing
   ├── Subnet: default
   ├── Public IP: Create new (Static)
   ├── NIC NSG: Advanced
   └── Configure NSG: See NSG section below

4. Management
   ├── Auto-shutdown: Enable (save costs - e.g., 8 PM)
   ├── Backup: Enable (optional but recommended)
   └── Boot diagnostics: Enable

5. Advanced
   └── Custom data (cloud-init): See Cloud-Init section

6. Tags
   ├── Environment: dev/prod
   └── Project: zuna
```

---

## Network Security (NSG)

### Recommended: Reverse Proxy Architecture

With Nginx reverse proxy, you only need to expose **3 ports**:

| Priority | Port | Protocol | Source       | Purpose                  |
|----------|------|----------|--------------|--------------------------|
| 100      | 22   | TCP      | Your IP only | SSH access               |
| 110      | 80   | TCP      | Any          | HTTP (redirect to HTTPS) |
| 120      | 443  | TCP      | Any          | HTTPS (all app traffic)  |

**That's it!** All other ports stay closed.

### Why Not Expose Application Ports?

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERNET                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                    ┌─────▼─────┐
                    │    NSG    │  Only allows: 22, 80, 443
                    └─────┬─────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      AZURE VM                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 NGINX (ports 80/443)                 │    │
│  │    Handles SSL, routing, rate limiting, auth         │    │
│  └───────┬──────────┬──────────┬──────────┬────────────┘    │
│          │          │          │          │                  │
│    ┌─────▼───┐ ┌────▼────┐ ┌───▼───┐ ┌───▼────┐            │
│    │Frontend │ │ Backend │ │Langfuse│ │LiteLLM │            │
│    │  :5173  │ │  :8000  │ │ :3000  │ │ :4000  │            │
│    └─────────┘ └─────────┘ └────────┘ └────────┘            │
│                                                              │
│    Internal only (never exposed to internet):                │
│    PostgreSQL:5432, Redis:6379, MSSQL:1433, ClickHouse:9000 │
└──────────────────────────────────────────────────────────────┘
```

### Benefits of Reverse Proxy

| Direct Port Exposure      | Via Reverse Proxy         |
|---------------------------|---------------------------|
| Multiple ports open (5+)  | Only 3 ports open         |
| No SSL on app ports       | SSL termination at Nginx  |
| No rate limiting          | Can add rate limiting     |
| Harder to add auth        | Easy to add basic auth    |
| Larger attack surface     | Minimal attack surface    |

### Service Access Summary

| Service         | Internal Port | Public Access              |
|-----------------|---------------|----------------------------|
| Frontend        | 5173          | `https://domain.com/`      |
| Backend API     | 8000          | `https://domain.com/api/`  |
| Langfuse        | 3000          | `https://domain.com/langfuse/` (auth protected) |
| LiteLLM         | 4000          | `https://domain.com/litellm/` (auth protected) |
| MinIO Console   | 9091          | `https://domain.com/minio/` (auth protected) |
| PostgreSQL      | 5432          | Not exposed (internal only) |
| Redis           | 6379          | Not exposed (internal only) |
| MSSQL           | 1433          | Not exposed (internal only) |
| ClickHouse      | 8123/9000     | Not exposed (internal only) |
| SQLPad          | 3010          | `https://domain.com/sqlpad/` (auth protected) |

---

## Reverse Proxy Setup

### Nginx Configuration

Create `/etc/nginx/sites-available/zuna`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name zuna.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# Main HTTPS server
server {
    listen 443 ssl http2;
    server_name zuna.yourdomain.com;

    # SSL certificates (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/zuna.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/zuna.yourdomain.com/privkey.pem;

    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend (React/Vite)
    location / {
        proxy_pass http://127.0.0.1:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Langfuse (protected with basic auth)
    location /langfuse/ {
        auth_basic "Langfuse Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:3000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # LiteLLM (protected with basic auth)
    location /litellm/ {
        auth_basic "LiteLLM Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:4000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # MinIO Console (protected with basic auth)
    location /minio/ {
        auth_basic "MinIO Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:9091/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SQLPad (protected with basic auth)
    location /sqlpad/ {
        auth_basic "SQLPad Admin";
        auth_basic_user_file /etc/nginx/.htpasswd;

        proxy_pass http://127.0.0.1:3010/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Create Basic Auth Password File

```bash
# Install apache2-utils for htpasswd
sudo apt install apache2-utils

# Create password file (you'll be prompted for password)
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Add more users
sudo htpasswd /etc/nginx/.htpasswd anotheruser
```

### Enable Nginx Site

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/zuna /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Domain & SSL Setup

### Option A: Custom Domain (Recommended)

1. **Configure DNS** (at your domain registrar):
   ```
   zuna.yourdomain.com  →  A Record  →  VM Public IP
   ```

2. **Get SSL Certificate** (after DNS propagation):
   ```bash
   sudo certbot --nginx -d zuna.yourdomain.com
   ```

3. **Auto-renewal** (already configured by Certbot):
   ```bash
   # Test renewal
   sudo certbot renew --dry-run
   ```

### Option B: Azure Public IP DNS

1. When creating Public IP, set DNS name label: `zuna-app`
2. Access via: `zuna-app.southeastasia.cloudapp.azure.com`
3. Get SSL:
   ```bash
   sudo certbot --nginx -d zuna-app.southeastasia.cloudapp.azure.com
   ```

---

## Cloud-Init Script

Paste this in **Advanced → Custom data** when creating the VM:

```yaml
#cloud-config
package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose-v2
  - git
  - nginx
  - certbot
  - python3-certbot-nginx
  - apache2-utils
  - ufw

runcmd:
  # Add user to docker group
  - usermod -aG docker azureuser

  # Enable and start Docker
  - systemctl enable docker
  - systemctl start docker

  # Format and mount data disk (assumes /dev/sdc)
  - |
    if [ -b /dev/sdc ]; then
      mkfs.ext4 -F /dev/sdc
      mkdir -p /data
      mount /dev/sdc /data
      echo '/dev/sdc /data ext4 defaults,nofail 0 2' >> /etc/fstab
    fi

  # Move Docker data to data disk
  - systemctl stop docker
  - mkdir -p /data/docker
  - |
    if [ -d /var/lib/docker ]; then
      rsync -a /var/lib/docker/ /data/docker/
      rm -rf /var/lib/docker
    fi
  - ln -s /data/docker /var/lib/docker
  - systemctl start docker

  # Configure UFW firewall
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow ssh
  - ufw allow 80/tcp
  - ufw allow 443/tcp
  - ufw --force enable

  # Create app directory
  - mkdir -p /data/apps
  - chown azureuser:azureuser /data/apps
```

---

## Post-Creation Setup

SSH into the VM and run:

```bash
# 1. Clone the repository
cd /data/apps
git clone https://github.com/pandalearnstocode/z.git zuna
cd zuna

# 2. Create and configure .env file
cp .env.example .env
nano .env  # Edit with your values

# 3. Fix line endings (if cloned on Windows)
sed -i 's/\r$//' scripts/postgres-init/*.sh

# 4. Start all services
docker compose up -d

# 5. Check all services are healthy
docker compose ps

# 6. Setup Nginx (copy config from Reverse Proxy section)
sudo nano /etc/nginx/sites-available/zuna

# 7. Create basic auth password
sudo htpasswd -c /etc/nginx/.htpasswd admin

# 8. Enable site
sudo ln -s /etc/nginx/sites-available/zuna /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# 9. Get SSL certificate
sudo certbot --nginx -d zuna.yourdomain.com

# 10. Verify everything works
curl -I https://zuna.yourdomain.com
```

---

## Cost Summary

### Infrastructure Costs

| Resource              | Monthly Cost |
|-----------------------|--------------|
| VM (D4as_v5)          | ~$125        |
| OS Disk (64GB P6)     | ~$10         |
| Data Disk (128GB P10) | ~$20         |
| Public IP (Static)    | ~$4          |
| Bandwidth (~100GB)    | ~$8          |
| **Subtotal**          | **~$167/month** |

### CI/CD Costs

| Resource              | Monthly Cost |
|-----------------------|--------------|
| Azure Container Registry (Basic) | ~$5  |
| ACR Storage (~5GB)    | ~$0.50       |
| GitHub Actions        | Free*        |
| **Subtotal**          | **~$6/month** |

*Free for public repos; 2,000 min/month for private repos

### Total Monthly Cost

| Scenario              | Monthly Cost |
|-----------------------|--------------|
| **Pay-as-you-go**     | **~$173/month** |
| **With 1-year Reserved VM** | **~$116/month** |
| **With Spot VM (dev only)** | **~$56/month** |

---

## Security Checklist

### VM Security
- [ ] SSH key authentication only (disable password login)
- [ ] NSG allows only ports 22, 80, 443
- [ ] SSH (port 22) restricted to your IP only
- [ ] UFW firewall enabled inside VM
- [ ] Admin UIs protected with basic auth
- [ ] SSL/TLS enabled with valid certificate
- [ ] Database ports not exposed publicly
- [ ] Regular OS updates enabled (`unattended-upgrades`)
- [ ] Backup enabled for data disk

### Application Security
- [ ] `.env` file not committed to git
- [ ] Docker images from trusted sources only
- [ ] Secrets rotated periodically
- [ ] ACR credentials stored securely on VM

### CI/CD Security
- [ ] GitHub secrets used (not hardcoded credentials)
- [ ] SSH deploy key is dedicated (not personal key)
- [ ] ACR admin credentials have minimal permissions
- [ ] Branch protection enabled on `develop`

---

## Spot VM & Auto-Shutdown

### Using Spot VMs (Dev/Test Only)

1. Go to **Azure Portal** → **Virtual machines** → **Create**
2. In **Pricing Options**, select **Spot**
3. Configure:
   - **Eviction Policy:** Deallocate (VM stops but can restart)
   - **Max Price:** Set your maximum hourly rate
4. **Savings:** 50-90% cheaper than regular VMs
5. **Risk:** VM can be evicted when Azure needs capacity

### Auto-Shutdown (Cost Savings)

1. Go to your VM's page in Azure Portal
2. Navigate to **Operations** → **Auto-shutdown**
3. Turn it **On**
4. Set **Shutdown time** (e.g., 7:00 PM)
5. Choose your **Timezone**
6. Optionally enable **Notification** email
7. Click **Save**

### Combining Spot + Auto-Shutdown

- Both features work together
- Use **Deallocate** eviction policy so VM can restart
- Auto-shutdown = scheduled daily stop
- Spot eviction = unpredictable stop when Azure needs capacity
- Great combination for dev/test environments

---

## Quick Reference

### Useful Commands

```bash
# Check all containers
docker compose ps

# View logs
docker compose logs -f [service_name]

# Restart a service
docker compose restart [service_name]

# Update and restart all
git pull
docker compose pull
docker compose up -d

# Check disk usage
df -h
docker system df

# Cleanup unused Docker resources
docker system prune -a
```

### Access URLs (with reverse proxy)

| Service   | URL                                    |
|-----------|----------------------------------------|
| Frontend  | `https://zuna.yourdomain.com/`         |
| Backend   | `https://zuna.yourdomain.com/api/`     |
| Langfuse  | `https://zuna.yourdomain.com/langfuse/`|
| LiteLLM   | `https://zuna.yourdomain.com/litellm/` |
| MinIO     | `https://zuna.yourdomain.com/minio/`   |
| SQLPad    | `https://zuna.yourdomain.com/sqlpad/`  |

---

## CI/CD with GitHub Actions

Automated deployment pipeline that builds Docker images only when needed, pushes to Azure Container Registry (ACR), and deploys to the VM.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Actions Workflow                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. PR Merged to develop                                                 │
│         │                                                                │
│         ▼                                                                │
│  2. Detect Changes ─────────────────────────────────────────────────┐   │
│         │                                                           │   │
│         ├── backend/* changed?  ──► Build backend image             │   │
│         ├── engine/* changed?   ──► Build engine image              │   │
│         ├── frontend/* changed? ──► Build frontend image            │   │
│         └── No changes?         ──► Skip build (save cost)          │   │
│                                                                      │   │
│  3. Build & Push (only changed images)                               │   │
│         │                                                            │   │
│         ├── Use Docker layer caching (save time & cost)             │   │
│         └── Push to Azure Container Registry                        │   │
│                                                                      │   │
│  4. Deploy to VM via SSH                                             │   │
│         │                                                            │   │
│         ├── Pull latest images from ACR                             │   │
│         └── Restart only changed services                           │   │
│                                                                      │   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Prerequisites Setup

#### Step 1: Create Azure Container Registry (ACR)

```bash
# Login to Azure CLI
az login

# Create resource group (if not exists)
az group create --name zuna-rg --location southeastasia

# Create Azure Container Registry (Basic tier for cost savings)
az acr create \
  --resource-group zuna-rg \
  --name zunaacr \
  --sku Basic \
  --admin-enabled true

# Get ACR credentials (save these for GitHub secrets)
az acr credential show --name zunaacr
```

**ACR Pricing (Basic tier):** ~$5/month + storage (~$0.10/GB)

#### Step 2: Configure VM for ACR Access

SSH into your VM and run:

```bash
# Login to ACR (run once to cache credentials)
# Replace with your ACR details
sudo docker login zunaacr.azurecr.io \
  --username zunaacr \
  --password <ACR_PASSWORD>

# Create deployment directory
mkdir -p /data/apps/zuna
cd /data/apps/zuna

# Create deploy script
sudo nano /usr/local/bin/deploy-zuna.sh
```

**Deploy script** (`/usr/local/bin/deploy-zuna.sh`):

```bash
#!/bin/bash
set -e

# Configuration
ACR_NAME="zunaacr.azurecr.io"
APP_DIR="/data/apps/zuna"
COMPOSE_FILE="$APP_DIR/docker-compose.prod.yml"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}[Deploy] Starting deployment...${NC}"

# Navigate to app directory
cd $APP_DIR

# Pull latest code
echo -e "${YELLOW}[Deploy] Pulling latest code...${NC}"
git pull origin develop

# Login to ACR
echo -e "${YELLOW}[Deploy] Logging into ACR...${NC}"
docker login $ACR_NAME --username $ACR_USERNAME --password $ACR_PASSWORD

# Pull latest images
echo -e "${YELLOW}[Deploy] Pulling latest images...${NC}"
docker compose -f $COMPOSE_FILE pull

# Restart services with new images
echo -e "${YELLOW}[Deploy] Restarting services...${NC}"
docker compose -f $COMPOSE_FILE up -d

# Cleanup old images
echo -e "${YELLOW}[Deploy] Cleaning up old images...${NC}"
docker image prune -f

# Health check
echo -e "${YELLOW}[Deploy] Running health checks...${NC}"
sleep 10
docker compose -f $COMPOSE_FILE ps

echo -e "${GREEN}[Deploy] Deployment complete!${NC}"
```

```bash
# Make script executable
sudo chmod +x /usr/local/bin/deploy-zuna.sh

# Create ACR credentials file (secure)
sudo nano /etc/zuna-acr-credentials
# Add:
# ACR_USERNAME=zunaacr
# ACR_PASSWORD=<your-acr-password>

sudo chmod 600 /etc/zuna-acr-credentials
```

#### Step 3: Setup SSH Key for GitHub Actions

```bash
# On your LOCAL machine, generate a deployment key
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/zuna_deploy_key

# Copy public key to VM
ssh-copy-id -i ~/.ssh/zuna_deploy_key.pub azureuser@<VM_IP>

# Test connection
ssh -i ~/.ssh/zuna_deploy_key azureuser@<VM_IP> "echo 'SSH works!'"

# Get private key content (add to GitHub secrets)
cat ~/.ssh/zuna_deploy_key
```

#### Step 4: Add GitHub Secrets

Go to **GitHub Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `ACR_LOGIN_SERVER` | `zunaacr.azurecr.io` | ACR login server |
| `ACR_USERNAME` | `zunaacr` | ACR admin username |
| `ACR_PASSWORD` | `<password>` | ACR admin password |
| `VM_HOST` | `<VM_PUBLIC_IP>` | VM public IP or hostname |
| `VM_USERNAME` | `azureuser` | VM SSH username |
| `VM_SSH_KEY` | `<private_key_content>` | SSH private key (entire content) |

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches:
      - develop
  pull_request:
    branches:
      - develop
    types: [closed]

env:
  ACR_LOGIN_SERVER: ${{ secrets.ACR_LOGIN_SERVER }}
  ACR_USERNAME: ${{ secrets.ACR_USERNAME }}
  ACR_PASSWORD: ${{ secrets.ACR_PASSWORD }}

jobs:
  # ============================================================================
  # Job 1: Detect which services have changed
  # ============================================================================
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.changes.outputs.backend }}
      engine: ${{ steps.changes.outputs.engine }}
      frontend: ${{ steps.changes.outputs.frontend }}
      any_changed: ${{ steps.changes.outputs.backend == 'true' || steps.changes.outputs.engine == 'true' || steps.changes.outputs.frontend == 'true' }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Detect file changes
        id: changes
        uses: dorny/paths-filter@v3
        with:
          filters: |
            backend:
              - 'backend/**'
              - 'dockerfiles/backend.Dockerfile'
              - 'pyproject.toml'
              - 'uv.lock'
            engine:
              - 'engine/**'
              - 'dockerfiles/engine.Dockerfile'
              - 'pyproject.toml'
              - 'uv.lock'
            frontend:
              - 'frontend/**'
              - 'dockerfiles/frontend.Dockerfile'
              - 'package.json'
              - 'package-lock.json'

      - name: Print detected changes
        run: |
          echo "Backend changed: ${{ steps.changes.outputs.backend }}"
          echo "Engine changed: ${{ steps.changes.outputs.engine }}"
          echo "Frontend changed: ${{ steps.changes.outputs.frontend }}"

  # ============================================================================
  # Job 2: Build and push Backend image (only if changed)
  # ============================================================================
  build-backend:
    runs-on: ubuntu-latest
    needs: detect-changes
    if: needs.detect-changes.outputs.backend == 'true'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to ACR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.ACR_LOGIN_SERVER }}
          username: ${{ env.ACR_USERNAME }}
          password: ${{ env.ACR_PASSWORD }}

      - name: Build and push Backend
        uses: docker/build-push-action@v5
        with:
          context: .
          file: dockerfiles/backend.Dockerfile
          push: true
          tags: |
            ${{ env.ACR_LOGIN_SERVER }}/zuna-backend:latest
            ${{ env.ACR_LOGIN_SERVER }}/zuna-backend:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.ACR_LOGIN_SERVER }}/zuna-backend:buildcache
          cache-to: type=registry,ref=${{ env.ACR_LOGIN_SERVER }}/zuna-backend:buildcache,mode=max

  # ============================================================================
  # Job 3: Build and push Engine image (only if changed)
  # ============================================================================
  build-engine:
    runs-on: ubuntu-latest
    needs: detect-changes
    if: needs.detect-changes.outputs.engine == 'true'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to ACR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.ACR_LOGIN_SERVER }}
          username: ${{ env.ACR_USERNAME }}
          password: ${{ env.ACR_PASSWORD }}

      - name: Build and push Engine
        uses: docker/build-push-action@v5
        with:
          context: .
          file: dockerfiles/engine.Dockerfile
          push: true
          tags: |
            ${{ env.ACR_LOGIN_SERVER }}/zuna-engine:latest
            ${{ env.ACR_LOGIN_SERVER }}/zuna-engine:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.ACR_LOGIN_SERVER }}/zuna-engine:buildcache
          cache-to: type=registry,ref=${{ env.ACR_LOGIN_SERVER }}/zuna-engine:buildcache,mode=max

  # ============================================================================
  # Job 4: Build and push Frontend image (only if changed)
  # ============================================================================
  build-frontend:
    runs-on: ubuntu-latest
    needs: detect-changes
    if: needs.detect-changes.outputs.frontend == 'true'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to ACR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.ACR_LOGIN_SERVER }}
          username: ${{ env.ACR_USERNAME }}
          password: ${{ env.ACR_PASSWORD }}

      - name: Build and push Frontend
        uses: docker/build-push-action@v5
        with:
          context: .
          file: dockerfiles/frontend.Dockerfile
          push: true
          tags: |
            ${{ env.ACR_LOGIN_SERVER }}/zuna-frontend:latest
            ${{ env.ACR_LOGIN_SERVER }}/zuna-frontend:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.ACR_LOGIN_SERVER }}/zuna-frontend:buildcache
          cache-to: type=registry,ref=${{ env.ACR_LOGIN_SERVER }}/zuna-frontend:buildcache,mode=max

  # ============================================================================
  # Job 5: Deploy to VM (only on push to develop, not PRs)
  # ============================================================================
  deploy:
    runs-on: ubuntu-latest
    needs: [detect-changes, build-backend, build-engine, build-frontend]
    # Run if any build succeeded OR if no changes detected (deploy config changes)
    if: |
      always() &&
      github.event_name == 'push' &&
      github.ref == 'refs/heads/develop' &&
      (needs.build-backend.result == 'success' || needs.build-backend.result == 'skipped') &&
      (needs.build-engine.result == 'success' || needs.build-engine.result == 'skipped') &&
      (needs.build-frontend.result == 'success' || needs.build-frontend.result == 'skipped')
    steps:
      - name: Deploy to VM via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.VM_HOST }}
          username: ${{ secrets.VM_USERNAME }}
          key: ${{ secrets.VM_SSH_KEY }}
          script: |
            set -e
            echo "=== Starting Deployment ==="

            # Source ACR credentials
            source /etc/zuna-acr-credentials

            # Navigate to app directory
            cd /data/apps/zuna

            # Pull latest code
            git pull origin develop

            # Login to ACR
            echo "Logging into ACR..."
            docker login ${{ secrets.ACR_LOGIN_SERVER }} \
              --username ${{ secrets.ACR_USERNAME }} \
              --password ${{ secrets.ACR_PASSWORD }}

            # Pull and restart only changed services
            echo "Pulling and restarting services..."

            if [ "${{ needs.detect-changes.outputs.backend }}" == "true" ]; then
              echo "Updating backend..."
              docker compose pull backend
              docker compose up -d backend
            fi

            if [ "${{ needs.detect-changes.outputs.engine }}" == "true" ]; then
              echo "Updating engine..."
              docker compose pull engine
              docker compose up -d engine
            fi

            if [ "${{ needs.detect-changes.outputs.frontend }}" == "true" ]; then
              echo "Updating frontend..."
              docker compose pull frontend
              docker compose up -d frontend
            fi

            # If no app changes, just pull latest compose and restart
            if [ "${{ needs.detect-changes.outputs.any_changed }}" != "true" ]; then
              echo "No app changes, checking for config updates..."
              docker compose up -d
            fi

            # Cleanup old images
            docker image prune -f

            # Show status
            docker compose ps

            echo "=== Deployment Complete ==="

      - name: Deployment Summary
        run: |
          echo "## Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Service | Changed | Action |" >> $GITHUB_STEP_SUMMARY
          echo "|---------|---------|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Backend | ${{ needs.detect-changes.outputs.backend }} | ${{ needs.detect-changes.outputs.backend == 'true' && 'Rebuilt & Deployed' || 'Skipped' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Engine | ${{ needs.detect-changes.outputs.engine }} | ${{ needs.detect-changes.outputs.engine == 'true' && 'Rebuilt & Deployed' || 'Skipped' }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Frontend | ${{ needs.detect-changes.outputs.frontend }} | ${{ needs.detect-changes.outputs.frontend == 'true' && 'Rebuilt & Deployed' || 'Skipped' }} |" >> $GITHUB_STEP_SUMMARY
```

### Production Docker Compose

Create `docker-compose.prod.yml` for production with ACR images:

```yaml
version: '3.8'

# Extends the base docker-compose.yml but uses ACR images instead of local builds

services:
  backend:
    image: ${ACR_LOGIN_SERVER:-zunaacr.azurecr.io}/zuna-backend:latest
    build: !reset null  # Disable local build
    # ... rest of config inherited from docker-compose.yml

  engine:
    image: ${ACR_LOGIN_SERVER:-zunaacr.azurecr.io}/zuna-engine:latest
    build: !reset null

  frontend:
    image: ${ACR_LOGIN_SERVER:-zunaacr.azurecr.io}/zuna-frontend:latest
    build: !reset null
```

Or update your main `docker-compose.yml` to use ACR images conditionally:

```yaml
services:
  backend:
    image: ${ACR_LOGIN_SERVER:-local}/zuna-backend:${IMAGE_TAG:-latest}
    build:
      context: .
      dockerfile: dockerfiles/backend.Dockerfile
    # ... rest of config
```

### Cost Optimization Summary

| Feature | Savings | Implementation |
|---------|---------|----------------|
| **Change Detection** | ~60-80% | Only build changed services |
| **Docker Layer Caching** | ~50-70% build time | Registry-based cache in ACR |
| **ACR Basic Tier** | ~$5/month | Sufficient for small teams |
| **Conditional Deploy** | ~40% deploy time | Only restart changed services |
| **Image Pruning** | Storage costs | Auto-cleanup old images |

### CI/CD Cost Estimate

| Resource | Cost |
|----------|------|
| GitHub Actions | Free (2,000 min/month for private repos) |
| ACR Basic | ~$5/month |
| ACR Storage (~5GB) | ~$0.50/month |
| **Total CI/CD** | **~$6/month** |

### Troubleshooting

#### Build Failures

```bash
# Check GitHub Actions logs
# Go to: Repo → Actions → Failed workflow → View logs

# Test Docker build locally
docker build -f dockerfiles/backend.Dockerfile -t test-backend .
```

#### Deployment Failures

```bash
# SSH into VM and check
ssh azureuser@<VM_IP>

# Check Docker status
docker compose ps
docker compose logs backend --tail 50

# Manual deploy
cd /data/apps/zuna
git pull
docker compose pull
docker compose up -d
```

#### ACR Authentication Issues

```bash
# On VM, re-authenticate to ACR
docker login zunaacr.azurecr.io \
  --username zunaacr \
  --password <ACR_PASSWORD>

# Verify login
docker pull zunaacr.azurecr.io/zuna-backend:latest
```

### Complete Setup Checklist

- [ ] **Azure Setup**
  - [ ] Create ACR (Basic tier)
  - [ ] Note ACR credentials
  - [ ] Add ACR login server to VM's Docker

- [ ] **VM Setup**
  - [ ] Create deploy script (`/usr/local/bin/deploy-zuna.sh`)
  - [ ] Store ACR credentials securely (`/etc/zuna-acr-credentials`)
  - [ ] Test Docker login to ACR

- [ ] **GitHub Setup**
  - [ ] Add all secrets (ACR_*, VM_*)
  - [ ] Create `.github/workflows/deploy.yml`
  - [ ] Generate and add SSH deploy key

- [ ] **Test Pipeline**
  - [ ] Make a small change to backend
  - [ ] Create PR and merge to develop
  - [ ] Verify only backend is rebuilt
  - [ ] Verify deployment succeeds

---

## Appendix: Complete File Structure

```
zuna/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD pipeline
├── backend/                        # Python FastAPI backend
├── engine/                         # Python FastAPI engine
├── frontend/                       # React/Vite frontend
├── dockerfiles/
│   ├── backend.Dockerfile
│   ├── engine.Dockerfile
│   └── frontend.Dockerfile
├── configs/
│   └── litellm/
│       └── config.yaml
├── scripts/
│   └── postgres-init/
│       └── 01-create-databases.sh
├── docker-compose.yml              # Main compose file
├── docker-compose.prod.yml         # Production compose (ACR images)
├── .env.example                    # Environment template
└── deployment.md                   # This file
```
