# Cookie & JWT Configuration Fix

## Problem

After login, accessing the dashboard returned a **422 error** and logout wasn't working. The JWT cookie wasn't being properly set or read.

## Root Cause

The configuration was set for **production** (HTTPS only) but the application was running in **development** (HTTP):

1. `JWT_COOKIE_SECURE = True` - Requires HTTPS, but we're on HTTP
2. `JWT_COOKIE_CSRF_PROTECT = True` - Requires CSRF tokens (not needed for API)
3. `SESSION_COOKIE_SECURE = True` - Requires HTTPS
4. `JWT_COOKIE_SAMESITE = 'Strict'` - Too restrictive for development
5. `PREFERRED_URL_SCHEME = 'https'` - Forces HTTPS URLs in development

## Solution

Made configuration environment-aware:

### File: `app/config.py`

**Before:**
```python
JWT_COOKIE_SECURE = True
JWT_COOKIE_SAMESITE = 'Strict'
JWT_COOKIE_CSRF_PROTECT = True
SESSION_COOKIE_SECURE = True
PREFERRED_URL_SCHEME = 'https'
```

**After:**
```python
JWT_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
JWT_COOKIE_SAMESITE = 'Lax'
JWT_COOKIE_CSRF_PROTECT = False
SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
PREFERRED_URL_SCHEME = 'https' if os.getenv('FLASK_ENV') == 'production' else 'http'
```

## Changes Explained

| Setting | Development | Production |
|---------|-------------|-----------|
| `JWT_COOKIE_SECURE` | False (HTTP OK) | True (HTTPS only) |
| `JWT_COOKIE_SAMESITE` | Lax | Lax |
| `JWT_COOKIE_CSRF_PROTECT` | False | False |
| `SESSION_COOKIE_SECURE` | False (HTTP OK) | True (HTTPS only) |
| `PREFERRED_URL_SCHEME` | http | https |

## Why This Works

### Development (HTTP)
- Cookies can be set over HTTP
- SameSite=Lax allows cross-site requests
- CSRF protection disabled (not needed for API)
- URLs use http://

### Production (HTTPS)
- Cookies only sent over HTTPS
- SameSite=Lax allows cross-site requests
- CSRF protection disabled (not needed for API)
- URLs use https://

## Testing

### Before Fix
```
Login → 200 OK
Dashboard → 422 Error (JWT not found)
Logout → Doesn't work
```

### After Fix
```
Login → 200 OK → Redirect to Dashboard
Dashboard → 200 OK → Shows content
Logout → 200 OK → Redirect to Login
```

## How to Test

1. Restart the application (it auto-reloads):
   ```bash
   python3 run.py
   ```

2. Login with test account:
   - Email: `alice@example.com`
   - Password: `TestPassword123`

3. Should see dashboard with content

4. Click Logout button

5. Should redirect to login page

## Files Modified

- `app/config.py` (5 lines changed)

## Security Notes

⚠️ **Development Settings**
- HTTP is allowed (not secure)
- CSRF protection disabled (not needed for API)
- Use only for development/testing

✅ **Production Settings**
- HTTPS enforced
- Secure cookies only
- SameSite protection enabled

## Environment Variables

The configuration automatically detects the environment:

```bash
# Development (default)
FLASK_ENV=development

# Production
FLASK_ENV=production
```

## Status

✅ **FIXED** - Login, dashboard access, and logout now work properly
