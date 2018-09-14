from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Apikey(models.Model):
    user = models.OneToOneField(User, related_name='api_key')
    key = models.BooleanField(default=False)
