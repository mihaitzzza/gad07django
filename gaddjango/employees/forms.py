from django import forms
from django.contrib.auth import get_user_model
from .models import Employee, Employer

AuthUserModel = get_user_model()


class UserNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class EmployerNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'employer']

    user = UserNameChoiceField(
        queryset=AuthUserModel.objects.filter(is_staff=False, employee__isnull=True).all()
    )
    employer = EmployerNameChoiceField(
        queryset=Employer.objects.all()
    )
