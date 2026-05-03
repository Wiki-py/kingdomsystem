from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Safely collect static files with verification'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Do NOT prompt the user for input of any kind.',
        )
    
    def handle(self, *args, **options):
        """Handle static file collection with safety checks"""
        
        self.stdout.write("=== Safe Static File Collection ===")
        
        # Check static files configuration
        self.stdout.write("Checking static files configuration...")
        
        if not hasattr(settings, 'STATICFILES_DIRS'):
            self.stdout.write(self.style.ERROR("STATICFILES_DIRS not configured"))
            return
        
        static_dirs = settings.STATICFILES_DIRS
        self.stdout.write(f"Static directories: {static_dirs}")
        
        # Check for logo file
        logo_found = False
        for static_dir in static_dirs:
            logo_path = static_dir / 'surveys' / 'logo' / 'obblogo.png'
            if logo_path.exists():
                self.stdout.write(self.style.SUCCESS(f"✓ Logo found at: {logo_path}"))
                logo_found = True
                break
        
        if not logo_found:
            self.stdout.write(self.style.WARNING("Logo file not found in expected locations"))
        
        # Collect static files
        self.stdout.write("Collecting static files...")
        
        try:
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS("✓ Static files collected successfully"))
            
            # Verify collection
            static_root = settings.STATIC_ROOT
            if static_root.exists():
                self.stdout.write(f"✓ Static files collected to: {static_root}")
                
                # Check if logo exists in collected static files
                collected_logo = static_root / 'surveys' / 'logo' / 'obblogo.png'
                if collected_logo.exists():
                    self.stdout.write(self.style.SUCCESS("✓ Logo available in static files"))
                else:
                    self.stdout.write(self.style.WARNING("Logo not found in collected static files"))
            else:
                self.stdout.write(self.style.ERROR("Static files directory not created"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error collecting static files: {e}"))
        
        self.stdout.write("=== Static file collection completed ===")
