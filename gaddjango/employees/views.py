from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from .models import Employer, Employee
from .forms import EmployeeForm

AuthUserModel = get_user_model()


# Create your views here.
def employees_home_view(request):
    return render(request, 'employees/homeview.html')


def add_employee(request):
    if request.method == 'GET':
        employee_form = EmployeeForm()

        return render(request, 'employees/add.html', {
            "form": employee_form,
        })
    if request.method == 'POST':
        employee_form = EmployeeForm(data=request.POST)
        if employee_form.is_valid():
            employee_form.save()

        return redirect(reverse("employees:add"))


def form_view(request):
    custom_text = request.POST.get("custom_text")
    print('custom_text', custom_text)
    return render(request, 'employees/add.html')


def list_users(request):
    users = AuthUserModel.objects.filter().all()
    return render(request, 'employees/users.html', {
        "users": users
    })


def view_user(request, user_id):
    user = get_object_or_404(AuthUserModel, pk=user_id)
    return HttpResponse(f'{user.id}: {user.first_name} {user.last_name}')
