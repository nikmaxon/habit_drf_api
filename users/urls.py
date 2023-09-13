from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('view/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_view'),
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(), name='user_edit'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
]
