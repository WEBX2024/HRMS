"""
Management command to create a test user
"""
from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Create a test user for development'

    def handle(self, *args, **options):
        email = 'mock@gmail.com'
        password = 'mock#1234'
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User {email} already exists'))
            return
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name='Mock',
            last_name='User',
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.email}'))
