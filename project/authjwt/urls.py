from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import get_current_user, UserList, lookup_email


urlpatterns = [
    path('jwt/obtain-token/', obtain_jwt_token),
    path('jwt/refresh-token/', refresh_jwt_token),
    path('jwt/verify-token/', verify_jwt_token),
    path('user/', get_current_user),
    path('users/', UserList.as_view()),
    path('lookup/', lookup_email),
]
