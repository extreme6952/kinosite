from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'account'

urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('register/',views.UserRegistrationView.as_view(),name='user_registration'),
    path('signup-confirm-activate/<uidb64>/<token>/',views.CustomRegistrationConfirmView.as_view(),name='signup_confirm'),
    path('sugnup-done/',views.CustomRegistrationDoneView.as_view(),name='signup_done'),
]
