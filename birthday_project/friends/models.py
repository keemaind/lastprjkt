from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)

    telegram_code = models.CharField(
        max_length=16,
        unique=True,
        default=uuid.uuid4().hex[:16]
    )
    def __str__(self):
        return f'{self.user.username} (Telegram: {self.telegram_id})'

class Friend(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    def __str__(self):
        return f'{self.name} ({self.birthday})'