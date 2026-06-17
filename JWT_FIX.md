# JWT Token Error Fix

## Problem

After successful login, the following error appeared:
```json
{
  "msg": "Subject must be a string"
}
```

## Root Cause

The JWT library (`flask-jwt-extended`) requires the `identity` parameter to be a **string**, but the code was passing an **integer** (user_id from database).

**File**: `app/routes/auth.py`
**Line**: 64

```python
# WRONG - passing integer
access_token = create_access_token(
    identity=user_data['user_id'],  # This is an integer
    additional_claims={'role': user_data['role'], 'name': user_data['full_name']}
)
```

## Solution

Convert the user_id to a string when creating the JWT token:

```python
# CORRECT - convert to string
access_token = create_access_token(
    identity=str(user_data['user_id']),  # Convert to string
    additional_claims={'role': user_data['role'], 'name': user_data['full_name']}
)
```

## Changes Made

### 1. Login Route (`app/routes/auth.py:64`)
**Before:**
```python
access_token = create_access_token(
    identity=user_data['user_id'],
    additional_claims={'role': user_data['role'], 'name': user_data['full_name']}
)
```

**After:**
```python
access_token = create_access_token(
    identity=str(user_data['user_id']),
    additional_claims={'role': user_data['role'], 'name': user_data['full_name']}
)
```

### 2. Get Current User Route (`app/routes/auth.py:91`)
**Before:**
```python
user_id = claims.get('sub')
user = User.get_by_id(user_id)
```

**After:**
```python
user_id = int(claims.get('sub'))  # Convert back to integer for database query
user = User.get_by_id(user_id)
```

## Why This Works

1. **JWT Creation**: JWT requires `identity` to be a string
2. **JWT Storage**: The identity is stored in the `sub` (subject) claim as a string
3. **Database Query**: The database expects an integer user_id
4. **Conversion**: Convert string → integer when retrieving user from database

## Testing

### Before Fix
```
Login → Error: "Subject must be a string"
```

### After Fix
```
Login → Success → Redirect to Dashboard
```

## Files Modified

- `app/routes/auth.py` (2 changes)

## Verification

To verify the fix works:

1. Start the application: `python3 run.py`
2. Login with test account: `alice@example.com / TestPassword123`
3. Should redirect to dashboard without error
4. Admin dashboard should load with statistics

## Related Issues

This fix also ensures:
- ✅ JWT tokens are properly created
- ✅ JWT tokens are properly validated
- ✅ User data is correctly retrieved from database
- ✅ Admin dashboard loads correctly
- ✅ All protected routes work properly

## Status

✅ **FIXED** - JWT token creation now works correctly
