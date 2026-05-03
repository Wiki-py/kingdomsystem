# Database Safety and Deployment Guide

## Overview
This guide ensures your Git pushes don't affect the deployed database on Render.

## Key Principles

### 1. Database Protection
- **Never commit database files** to Git (.gitignore prevents this)
- **Use environment variables** for database configuration
- **Handle migrations carefully** on production

### 2. Environment Separation
- **Development**: Local SQLite database
- **Production**: Render PostgreSQL database
- **Settings**: Environment-specific configurations

## Deployment Safety Checklist

### Before Pushing to Git:
1. ✅ Database files are in .gitignore
2. ✅ Environment variables are not committed
3. ✅ Local database changes won't affect production
4. ✅ Static files are collected separately

### During Deployment:
1. ✅ Render uses production database (PostgreSQL)
2. ✅ Migrations run automatically if needed
3. ✅ Static files are collected on server
4. ✅ Environment variables are loaded from Render

### After Deployment:
1. ✅ Production database remains intact
2. ✅ Local development database unchanged
3. ✅ Code updates without data loss

## Migration Strategy

### Safe Migration Process:
1. **Test migrations locally first**
2. **Backup production database** (if needed)
3. **Deploy code changes**
4. **Let Render handle migrations automatically**
5. **Monitor deployment logs**

### Migration Commands:
```bash
# Local testing
python manage.py makemigrations
python manage.py migrate

# Production (handled by Render)
# Render automatically runs: python manage.py migrate
```

## Environment Configuration

### Development (.env):
```
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=your-local-secret-key
```

### Production (Render Environment Variables):
```
DEBUG=False
DATABASE_URL=postgresql://render-database-url
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-app.onrender.com
```

## Git Safety Features

### .gitignore Protections:
- Database files (*.sqlite3, *.db)
- Environment files (.env)
- Local settings (local_settings.py)
- Static files (staticfiles/, media/)
- Backup files (*.backup, *.dump)

### What IS in Git:
- Migration files (for team collaboration)
- Model definitions
- Settings structure
- Code changes

## Render Deployment Process

### Automatic Steps:
1. Code is pushed to GitHub
2. Render detects changes
3. Builds the application
4. Runs migrations (if needed)
5. Collects static files
6. Starts the application

### Database Safety:
- **Production database is separate** from local
- **Migrations are applied to production only**
- **Local database remains unchanged**
- **Data is preserved across deployments**

## Emergency Procedures

### If Migration Fails:
1. Check Render deployment logs
2. Rollback to previous commit
3. Fix migration issues locally
4. Test and redeploy

### If Database Issues:
1. Contact Render support
2. Check database connection
3. Verify environment variables
4. Restore from backup if needed

## Best Practices

### Development:
- Use local database for testing
- Test migrations before deploying
- Keep database changes minimal
- Backup important data

### Production:
- Monitor deployment logs
- Use environment variables
- Never manually modify production database
- Keep regular backups

### Git Workflow:
- Commit code changes only
- Never commit database files
- Use feature branches for testing
- Review changes before merging

## Summary

Your deployed database is protected because:
1. **Database files are excluded from Git**
2. **Production uses separate PostgreSQL database**
3. **Environment variables configure connections**
4. **Render handles migrations automatically**
5. **Local and production databases are completely separate**

This ensures your Git pushes only affect code, not data.
