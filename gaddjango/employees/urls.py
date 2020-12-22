from django.urls import path
from .views import employees_home_view, add_employee, list_users, view_user

app_name = 'employees'


urlpatterns = [
    path('', employees_home_view, name="homeview"),
    path('add/', add_employee, name="add"),
    path('users/', list_users, name='user_list'),
    path('users/<int:user_id>/', view_user, name='view_user')
]
