from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser if it does not exist"

    def handle(self, *args, **kwargs):
        user_mng = get_user_model()
        if not user_mng.objects.filter(is_superuser=True).exists():
            username = "qustoo"
            email = "qusto@yandex.ru"
            password = "123"
            user_mng.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))
