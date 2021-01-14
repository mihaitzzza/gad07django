from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

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

    owner = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, unique=True)
    employees = models.ManyToManyField(AuthUserModel, through='Employee', related_name='employees')

    def owner_full_name(self):
        return "%s %s" % (self.owner.first_name, self.owner.last_name)
    owner_full_name.short_description = "Owner"

    def employees_number(self):
        return self.employees.count()
    employees_number.short_description = "# Employees"

    def __str__(self):
        return "[ID=%s, TYPE=%s] %s" % (self.id, type(self), self.name)


class Employee(BaseModel):
    class Meta:
        db_table = 'employees'

    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    wage = models.IntegerField(default=50, validators=[MinValueValidator(0)])

    # 'first_name', 'last_name', 'email', 'employer',
    def first_name(self):
        return self.user.first_name
    first_name.admin_order_field = 'user__first_name'

    def last_name(self):
        return self.user.last_name
    last_name.admin_order_field = 'user__last_name'

    def email(self):
        return self.user.email
    email.admin_order_field = 'user__email'

    def employer_name(self):
        return self.employer.name
    employer_name.admin_order_field = 'employer__name'
