# Aiven Database Setup Guide

This guide explains how to set up a MySQL database on Aiven and connect your Digital Attendance System to it.

## Prerequisites
- Aiven account (sign up at https://aiven.io/)
- Basic understanding of database concepts

## Step 1: Create a MySQL Service on Aiven

1. Log in to your Aiven console
2. Click **"Create Service"**
3. Select **"MySQL"** as the service type
4. Choose a cloud provider and region (e.g., AWS, Google Cloud, Azure)
5. Select a service plan (free tier available for testing)
6. Enter a service name (e.g., `attendance-db`)
7. Click **"Create Service"**

## Step 2: Get Connection Details

Once your service is running:

1. Go to your service dashboard
2. Click on the **"Connection Information"** tab
3. Copy the following details:
   - **Host** (e.g., `mysql-xxxxx.aivencloud.com`)
   - **Port** (usually 25060 for Aiven MySQL)
   - **User** (e.g., `avnadmin`)
   - **Password** (click to reveal)
   - **Database Name** (usually `defaultdb`)

## Step 3: Download SSL Certificates

Aiven requires SSL connections:

1. In the Connection Information tab, find the **"CA Certificate"** section
2. Download the CA certificate file
3. Save it as `ca.pem` in your project root

## Step 4: Update Environment Variables

Update your `.env` file with the Aiven connection details:

```bash
# Database Configuration
DB_HOST=mysql-xxxxx.aivencloud.com
DB_USER=avnadmin
DB_PASSWORD=your-aiven-password
DB_NAME=defaultdb
DB_PORT=25060

# Database SSL Configuration
DB_SSL=true
DB_SSL_CA=/path/to/ca.pem
DB_SSL_CERT=
DB_SSL_KEY=
```

**Important:** Replace the placeholder values with your actual Aiven credentials.

## Step 5: Run Database Migrations

Since you're switching databases, you need to recreate the schema:

```bash
# Run the database initialization script
python init_db.py
```

Or manually run the SQL from `migrations/schema.sql`:

```bash
mysql -h mysql-xxxxx.aivencloud.com -P 25060 -u avnadmin -p defaultdb < migrations/schema.sql
```

## Step 6: Test the Connection

Start your application:

```bash
source venv/bin/activate
python run.py
```

Check the logs for any database connection errors. If successful, the app will start normally.

## SSL Certificate Notes

- Aiven provides a CA certificate for SSL connections
- The certificate path should be absolute or relative to your project root
- If using Aiven's free tier, you only need the CA certificate
- For paid tiers with client certificates, also set `DB_SSL_CERT` and `DB_SSL_KEY`

## Troubleshooting

### Connection Timeout
- Check if your IP is whitelisted in Aiven service settings
- Verify the host and port are correct
- Ensure SSL is enabled (`DB_SSL=true`)

### SSL Errors
- Verify the CA certificate path is correct
- Ensure the certificate file is readable
- Check that `DB_SSL=true` is set

### Authentication Errors
- Verify username and password from Aiven console
- Check that the database name is correct
- Ensure the user has proper permissions

## Production Considerations

1. **Environment Variables**: Never commit `.env` to version control
2. **Secrets Management**: Use Aiven's integration with secret managers for production
3. **Backups**: Aiven automatically handles backups, but verify your backup schedule
4. **High Availability**: Consider using Aiven's HA plans for production
5. **Monitoring**: Set up Aiven's monitoring and alerting

## Migration from Local MySQL

If migrating from a local MySQL database:

1. Export your local data:
   ```bash
   mysqldump -u root -p attendance_db > backup.sql
   ```

2. Import to Aiven:
   ```bash
   mysql -h mysql-xxxxx.aivencloud.com -P 25060 -u avnadmin -p defaultdb < backup.sql
   ```

3. Update your `.env` file with Aiven credentials

## Cost Considerations

- Aiven offers a free tier for MySQL (limited resources)
- Paid tiers start at approximately $49/month (varies by region)
- Consider your expected traffic and storage needs when choosing a plan
