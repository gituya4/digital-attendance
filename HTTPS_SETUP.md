# HTTPS Setup Guide for Mobile Camera Access

## ⚠️ Important: HTTPS is Required for QR Scanning

Mobile browsers require **HTTPS (secure connection)** to access the device camera via `getUserMedia()`. This is a browser security requirement, not optional.

**The student QR scanning feature will NOT work without HTTPS.**

---

## Development Setup (Self-Signed Certificate)

For testing on localhost with HTTPS:

### 1. Generate Self-Signed Certificate

```bash
# Generate private key and certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# When prompted, enter:
# Country: KE
# State: Nakuru
# Locality: Nakuru
# Organization: Kabarak University
# Common Name: localhost
```

### 2. Run Flask with SSL

```bash
# Using Flask development server with SSL
python -c "
from app import create_app
app = create_app()
app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000)
"
```

### 3. Access Application

```
https://localhost:5000
```

**Note**: Browser will show security warning (expected for self-signed cert). Click "Advanced" → "Proceed anyway"

---

## Production Setup (Let's Encrypt)

### Prerequisites
- Domain name (e.g., `attendance.university.ac.ke`)
- VPS or dedicated server
- Ubuntu 22.04 LTS recommended

### 1. Install Certbot

```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
```

### 2. Obtain SSL Certificate

```bash
# Standalone mode (if Nginx not running yet)
sudo certbot certonly --standalone -d attendance.university.ac.ke

# Or with Nginx (if already running)
sudo certbot --nginx -d attendance.university.ac.ke
```

### 3. Configure Nginx

Create `/etc/nginx/sites-available/attendance`:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name attendance.university.ac.ke;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name attendance.university.ac.ke;
    
    # SSL Certificate
    ssl_certificate /etc/letsencrypt/live/attendance.university.ac.ke/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/attendance.university.ac.ke/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Static files
    location /static/ {
        alias /home/ubuntu/digital-attendance/app/static/;
        expires 30d;
    }
}
```

### 4. Enable Nginx Site

```bash
sudo ln -s /etc/nginx/sites-available/attendance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Auto-Renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically sets up renewal via systemd timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Gunicorn Configuration

### Create Systemd Service File

Create `/etc/systemd/system/attendance.service`:

```ini
[Unit]
Description=Digital Attendance System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/digital-attendance
Environment="PATH=/home/ubuntu/digital-attendance/venv/bin"
ExecStart=/home/ubuntu/digital-attendance/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/attendance/access.log \
    --error-logfile /var/log/attendance/error.log \
    run:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable attendance
sudo systemctl start attendance
sudo systemctl status attendance
```

---

## Environment Configuration

Update `.env` for production:

```bash
FLASK_ENV=production
FLASK_DEBUG=False

# Database
DB_HOST=localhost
DB_USER=attendance_user
DB_PASSWORD=strong_password_here
DB_NAME=attendance_db

# Secrets (generate with: python -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET_KEY=your-generated-secret-key
HMAC_SECRET_KEY=your-generated-hmac-key

# Application
APP_DOMAIN=attendance.university.ac.ke
PREFERRED_URL_SCHEME=https

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## Testing HTTPS Setup

### 1. Test Certificate

```bash
# Check certificate details
openssl x509 -in /etc/letsencrypt/live/attendance.university.ac.ke/fullchain.pem -text -noout

# Check certificate expiry
openssl x509 -enddate -noout -in /etc/letsencrypt/live/attendance.university.ac.ke/fullchain.pem
```

### 2. Test HTTPS Connection

```bash
# Using curl
curl -I https://attendance.university.ac.ke

# Using openssl
openssl s_client -connect attendance.university.ac.ke:443
```

### 3. Test Mobile Camera Access

1. Open browser on mobile phone
2. Navigate to `https://attendance.university.ac.ke`
3. Login as student
4. Click QR scanner button
5. Grant camera permission when prompted
6. Verify camera feed appears

---

## Troubleshooting

### Certificate Issues

**Problem**: "SSL certificate problem"
```bash
# Verify certificate chain
openssl verify -CAfile /etc/letsencrypt/live/attendance.university.ac.ke/chain.pem \
    /etc/letsencrypt/live/attendance.university.ac.ke/fullchain.pem
```

**Problem**: Certificate expired
```bash
# Renew manually
sudo certbot renew --force-renewal
sudo systemctl restart nginx
```

### Camera Access Issues

**Problem**: "Camera access denied" on mobile
- Ensure HTTPS is being used (check URL bar)
- Check browser permissions for camera
- Try different browser (Chrome, Firefox, Safari)
- Ensure device has camera hardware

**Problem**: "getUserMedia not available"
- Verify HTTPS is enabled
- Check browser console for errors
- Ensure browser supports WebRTC

### Nginx Issues

**Problem**: "502 Bad Gateway"
```bash
# Check Gunicorn is running
sudo systemctl status attendance

# Check Nginx error log
sudo tail -f /var/log/nginx/error.log

# Restart services
sudo systemctl restart attendance
sudo systemctl restart nginx
```

---

## Security Checklist

- [x] HTTPS enforced (HTTP redirects to HTTPS)
- [x] Valid SSL certificate (Let's Encrypt)
- [x] Security headers configured
- [x] TLS 1.2+ only
- [x] Strong ciphers configured
- [x] HSTS enabled
- [x] Certificate auto-renewal enabled
- [x] Firewall rules configured
- [x] Regular backups enabled

---

## Performance Optimization

### Enable Compression

Add to Nginx config:

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

### Enable Caching

Add to Nginx config:

```nginx
location /static/ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### Monitor Performance

```bash
# Check Gunicorn workers
ps aux | grep gunicorn

# Monitor system resources
top
htop

# Check Nginx status
sudo systemctl status nginx
```

---

## Important Notes

⚠️ **HTTPS is NOT optional** for mobile camera access
- All student QR scanning requires HTTPS
- Browsers block camera access on HTTP
- Use Let's Encrypt for free SSL certificates
- Certificate renewal is automatic with Certbot

✅ **Best Practices**
- Always use HTTPS in production
- Keep certificates updated
- Monitor certificate expiry
- Use strong TLS versions
- Enable security headers
- Regular security audits

---

## Support

For HTTPS issues:
1. Check Nginx error logs: `/var/log/nginx/error.log`
2. Check Gunicorn logs: `/var/log/attendance/error.log`
3. Verify certificate: `openssl x509 -text -noout -in cert.pem`
4. Test connectivity: `curl -I https://your-domain.com`

---

**Remember**: Without HTTPS, students cannot scan QR codes on their phones!
