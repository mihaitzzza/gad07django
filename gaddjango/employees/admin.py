from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Employer, Employee

AuthUserModel = get_user_model()


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_full_name', 'employees_number')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        return queryset.filter(owner=request.user)

    def get_fields(self, request, obj=None):
        all_fields = super().get_fields(request, obj)

        if not request.user.is_superuser:
            all_fields.remove('owner')

        return all_fields

    def save_model(self, request, obj, form, change):
        if not obj.pk and not request.user.is_superuser:
            obj.owner = request.user

        return super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            kwargs['queryset'] = AuthUserModel.objects.filter(is_staff=True, is_superuser=False)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'employer_name', 'wage',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        return queryset.filter(employer__owner=request.user)
