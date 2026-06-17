# HTTPS & Mobile Scanning Changes

## Summary of Updates

This document outlines the critical changes made to ensure the system works properly with mobile phone QR scanning, which requires HTTPS.

---

## Changes Made

### 1. Configuration Updates (`app/config.py`)

**Changed:**
```python
JWT_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
```

**To:**
```python
JWT_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
PREFERRED_URL_SCHEME = 'https'
```

**Reason:** Force HTTPS for all environments to ensure mobile camera access works. Browsers block camera access on HTTP connections.

---

### 2. HTTPS Enforcement Middleware (`app/__init__.py`)

**Added:**
```python
@app.before_request
def enforce_https():
    if app.config['FLASK_ENV'] == 'production':
        if not request.is_secure and request.headers.get('X-Forwarded-Proto', 'http') != 'https':
            url = request.url.replace('http://', 'https://', 1)
            return redirect(url, code=301)
```

**Reason:** Automatically redirect HTTP requests to HTTPS in production. This ensures students accessing the system on mobile phones are always on a secure connection.

---

### 3. Environment Configuration (`.env.example`)

**Changed:**
- `FLASK_ENV=development` → `FLASK_ENV=production`
- `FLASK_DEBUG=True` → `FLASK_DEBUG=False`
- `MAIL_USERNAME=your-email@gmail.com` → `MAIL_USERNAME=your-gmail-account@gmail.com`

**Added:**
- `PREFERRED_URL_SCHEME=https`
- Detailed comments for each configuration
- Secret key generation instructions

**Reason:** 
- Use generic Gmail format (not Kabarak-specific)
- Production-ready defaults
- Clear documentation for setup

---

### 4. Student Dashboard UI (`app/templates/student/dashboard.html`)

**Added:**
```html
<div id="httpsWarning" style="display: none; ...">
    <strong>⚠️ HTTPS Required:</strong> Camera access requires a secure HTTPS connection...
</div>
```

**Added to `initCamera()` function:**
```javascript
if (location.protocol !== 'https:') {
    document.getElementById('httpsWarning').style.display = 'block';
    Toast.error('Camera access requires HTTPS. Please use a secure connection.');
    return;
}
```

**Reason:** 
- Warn students if they try to use camera on HTTP
- Prevent confusing camera permission errors
- Clear error message explaining the requirement

---

## Why These Changes Are Critical

### Mobile Camera Access Requirements

Modern browsers (Chrome, Firefox, Safari) require **HTTPS** to access device camera for security reasons:

1. **Security**: HTTPS ensures encrypted communication
2. **Privacy**: Prevents man-in-the-middle attacks on camera data
3. **Browser Policy**: Browsers block `getUserMedia()` on HTTP

### Student Workflow Impact

**Before (Without HTTPS):**
- Student tries to scan QR code
- Browser blocks camera access
- Student sees cryptic error
- Attendance marking fails

**After (With HTTPS):**
- Student accesses system via HTTPS
- Camera permission request appears
- Student grants permission
- QR scanning works smoothly

---

## Deployment Instructions

### For Development (Testing)

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
python -c "
from app import create_app
app = create_app()
app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000)
"

# Access at: https://localhost:5000
```

### For Production

```bash
# 1. Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# 2. Get Let's Encrypt certificate
sudo certbot certonly --standalone -d your-domain.com

# 3. Configure Nginx with SSL
# See HTTPS_SETUP.md for full configuration

# 4. Run Gunicorn behind Nginx
gunicorn -w 4 -b 127.0.0.1:5000 run:app

# 5. Nginx handles HTTPS and proxies to Gunicorn
```

---

## Email Configuration

### Gmail Setup (Generic Format)

The system now uses generic Gmail format instead of Kabarak-specific:

```
MAIL_USERNAME=your-gmail-account@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

**Steps to configure:**
1. Enable 2-Factor Authentication on Gmail account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password in `.env`

**Example:**
```
MAIL_USERNAME=attendance.system@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
```

---

## Testing HTTPS Setup

### Verify HTTPS is Working

```bash
# Test certificate
openssl x509 -in cert.pem -text -noout

# Test connection
curl -I https://localhost:5000

# Test from mobile
# 1. Get your computer's IP: ifconfig
# 2. On mobile: https://YOUR_IP:5000
# 3. Accept certificate warning
# 4. Try QR scanning
```

### Verify Mobile Camera Access

1. Open browser on mobile phone
2. Navigate to `https://your-domain.com`
3. Login as student
4. Click QR scanner button (📱)
5. Grant camera permission
6. Verify camera feed appears
7. Scan QR code from lecturer

---

## Security Implications

✅ **Improved Security:**
- All data encrypted in transit
- Camera access protected
- Prevents man-in-the-middle attacks
- Complies with browser security policies

✅ **Production Ready:**
- Automatic HTTP → HTTPS redirect
- Let's Encrypt certificate support
- Auto-renewal capability
- Security headers configured

---

## Backward Compatibility

These changes are **backward compatible**:
- Existing API endpoints work the same
- Database schema unchanged
- Authentication logic unchanged
- Only adds HTTPS requirement for mobile scanning

---

## Troubleshooting

### "Camera access denied" on mobile

**Solution:**
1. Verify URL uses HTTPS (check address bar)
2. Check browser permissions for camera
3. Try different browser
4. Check device has camera hardware

### "Certificate error" on mobile

**Solution:**
1. For self-signed: Accept the warning
2. For Let's Encrypt: Verify domain is correct
3. Check certificate hasn't expired
4. Restart Nginx/Gunicorn

### "HTTPS not working" on localhost

**Solution:**
```bash
# Generate new certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run Flask with SSL
python -c "
from app import create_app
app = create_app()
app.run(ssl_context=('cert.pem', 'key.pem'), port=5000)
"
```

---

## Files Modified

1. `app/config.py` - HTTPS enforcement configuration
2. `app/__init__.py` - HTTPS redirect middleware
3. `.env.example` - Production-ready environment template
4. `app/templates/student/dashboard.html` - HTTPS warning and check

## Files Created

1. `HTTPS_SETUP.md` - Comprehensive HTTPS setup guide
2. `HTTPS_CHANGES.md` - This file

---

## Next Steps

1. **Development**: Use self-signed certificate for testing
2. **Staging**: Test with Let's Encrypt certificate
3. **Production**: Deploy with proper SSL certificate
4. **Monitoring**: Monitor certificate expiry and renewal

---

## Important Reminders

⚠️ **HTTPS is NOT optional**
- Mobile camera access requires HTTPS
- Students cannot scan QR codes on HTTP
- Always deploy with valid SSL certificate

✅ **Best Practices**
- Use Let's Encrypt for free certificates
- Enable auto-renewal
- Monitor certificate expiry
- Keep TLS versions updated
- Enable security headers

---

**Status**: System now fully supports mobile QR scanning with HTTPS requirement enforced.
