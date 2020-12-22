from django.db import models
from django.contrib.auth import get_user_model

AuthUserModel = get_user_model()


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Employer(BaseModel):
    class Meta:
        db_table = 'employers'

    name = models.CharField(max_length=255, unique=True)


class Employee(BaseModel):
    class Meta:
        db_table = 'employees'

    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    wage = models.IntegerField(default=50)
