from django.core.management.base import BaseCommand
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup database'

    def handle(self, *args, **kwargs):
        backup_dir = 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(backup_dir, filename)

        os.system(f'python manage.py dumpdata > {filepath}')

        self.stdout.write(self.style.SUCCESS(f'Backup created: {filepath}'))