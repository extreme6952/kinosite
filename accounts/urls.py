from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'account'

urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('register/',views.UserRegistrationView.as_view(),name='user_registration'),
]
