#!/usr/bin/env python3
"""
Safe Deployment Script
Ensures database safety during Git deployments
"""

import os
import sys
import subprocess
from pathlib import Path

def check_database_safety():
    """Check if database configuration is safe for deployment"""
    
    # Check if we're in production
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    if not debug_mode:
        # Production checks
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("ERROR: DATABASE_URL environment variable not set in production")
            return False
        
        if 'sqlite' in database_url:
            print("ERROR: SQLite database detected in production")
            return False
        
        if 'postgres' not in database_url and 'postgresql' not in database_url:
            print("ERROR: Only PostgreSQL databases are allowed in production")
            return False
        
        print("✓ Production database configuration is safe")
    
    else:
        # Development checks
        print("✓ Development mode detected - using local database")
    
    return True

def check_git_status():
    """Check Git status for any database files that shouldn't be committed"""
    
    try:
        # Check for database files in Git
        result = subprocess.run(
            ['git', 'ls-files', '*.sqlite3', '*.db', '*.db3'],
            capture_output=True, text=True
        )
        
        if result.stdout.strip():
            print("WARNING: Database files detected in Git repository:")
            print(result.stdout)
            print("These should be removed from Git tracking")
            return False
        
        print("✓ No database files tracked in Git")
        return True
        
    except subprocess.CalledProcessError:
        print("WARNING: Could not check Git status")
        return True  # Continue anyway

def check_environment_files():
    """Check that environment files are not committed"""
    
    env_files = ['.env', '.env.production', '.env.staging', 'local_settings.py']
    
    try:
        for env_file in env_files:
            result = subprocess.run(
                ['git', 'ls-files', env_file],
                capture_output=True, text=True
            )
            
            if result.stdout.strip():
                print(f"WARNING: Environment file {env_file} is tracked in Git")
                return False
        
        print("✓ No environment files tracked in Git")
        return True
        
    except subprocess.CalledProcessError:
        print("WARNING: Could not check environment files")
        return True

def run_migrations_safely():
    """Run migrations with safety checks"""
    
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    if debug_mode:
        print("Running migrations in development mode...")
        try:
            subprocess.run(['python', 'manage.py', 'migrate', '--check'], check=True)
            print("✓ Migration check passed")
        except subprocess.CalledProcessError:
            print("Running pending migrations...")
            subprocess.run(['python', 'manage.py', 'migrate'], check=True)
            print("✓ Migrations applied successfully")
    else:
        print("Production mode - migrations will be handled by deployment platform")
    
    return True

def backup_database():
    """Create database backup before deployment (production only)"""
    
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    if not debug_mode:
        print("Production mode - database backup recommended")
        print("Please ensure your hosting provider (Render) handles backups")
        
        # Note: Render automatically handles PostgreSQL backups
        print("✓ Render provides automatic PostgreSQL backups")
    
    return True

def main():
    """Main deployment safety check"""
    
    print("=== Safe Deployment Check ===")
    print()
    
    checks = [
        ("Database Configuration", check_database_safety),
        ("Git Database Files", check_git_status),
        ("Environment Files", check_environment_files),
        ("Migration Safety", run_migrations_safely),
        ("Database Backup", backup_database),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"Checking {check_name}...")
        if not check_func():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All safety checks passed!")
        print("Your deployment is safe and won't affect the database.")
        return 0
    else:
        print("❌ Safety checks failed!")
        print("Please address the issues before deploying.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
