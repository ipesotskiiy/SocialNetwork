from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import RegisterUserAPIView, MyTokenObtainPairView

app_name = 'users'

urlpatterns = [
    path('auth/signin', MyTokenObtainPairView.as_view(), name='signin'),
    path('api/token/refresh/', TokenRefreshView.as_view(), имя='token_refresh'),
    path('auth/signup', RegisterUserAPIView.as_view(), name='signup')
]
