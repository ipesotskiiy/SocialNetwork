from django.urls import path

from users.views import RegisterUserAPIView

app_name = 'users'

urlpatterns = [
    path('auth/signup', RegisterUserAPIView.as_view(), name='signup')
]