from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from employees.models import Employer, Employee

AuthUserModel = get_user_model()

generic_permissions = {'add', 'change', 'view', 'delete'}
employer_model_name = Employer.__name__.lower()
employee_model_name = Employee.__name__.lower()


def get_permissions_str():
    permissions = set()

    for model_name in [employer_model_name, employee_model_name]:
        for permission in generic_permissions:
            permissions.add("%s_%s" % (permission, model_name))

    return permissions


class Command(BaseCommand):
    def handle(self, *args, **options):
        owners_group = Group.objects.filter(name="Owners").first()

        if owners_group is None:
            # Create "Owners" group.
            owners_group = Group(name="Owners")
            owners_group.save()
        # print('owners_group', owners_group)

        permissions_str = get_permissions_str()
        # print('permissions', permissions_str)

        permissions_db = Permission.objects.filter(codename__in=permissions_str).all()
        # print('permissions_db', permissions_db)

        for permission in permissions_db:
            owners_group.permissions.add(permission)

        staff_users = AuthUserModel.objects.filter(is_staff=True, is_superuser=False).all()
        for user in staff_users:
            user.groups.add(owners_group)

