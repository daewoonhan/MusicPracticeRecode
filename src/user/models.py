from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  user_id = models.AutoField(primary_key=True)
  id = models.CharField(max_length=50, unique=True, db_index=True)
  password = models.CharField(max_length=255)
  name = models.CharField(max_length=50)
  email = models.CharField(max_length=100, unique=True)
  introduction = models.CharField(max_length=255, null=True, blank=True)

  useranme = None

  REQUIRED_FIELDS = []
  USERNAME_FIELD = 'id'
  class Meta:
    db_table = "custom_user"