import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create the initial deployment administrator when credentials are configured.'

    def handle(self, *args, **options):
        values = {
            'username': os.environ.get('DJANGO_SUPERUSER_USERNAME', ''),
            'email': os.environ.get('DJANGO_SUPERUSER_EMAIL', ''),
            'password': os.environ.get('DJANGO_SUPERUSER_PASSWORD', ''),
        }
        if not any(values.values()):
            return
        if not all(values.values()):
            raise CommandError(
                'Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, and '
                'DJANGO_SUPERUSER_PASSWORD together.'
            )

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        username = values.pop('username')
        try:
            user_model._default_manager.get_by_natural_key(username)
        except user_model.DoesNotExist:
            user_model._default_manager.create_superuser(
                **{username_field: username, **values}
            )
            self.stdout.write('Initial administrator created.')
        else:
            self.stdout.write('Initial administrator already exists.')
