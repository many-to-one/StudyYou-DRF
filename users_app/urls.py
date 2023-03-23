from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email_verify/', VerifyEmail.as_view(), name='email_verify'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/<pk>/', LogoutView.as_view(), name="logout"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('mapp/password-reset-complete/<pk>/', password_change, name='password_change'),
    path('success/', success, name='success'),
    path('user/<pk>/', UserView.as_view(), name='user'),
    path('users/<congregation>/', AllUsers.as_view(), name='users'),
    path('users_by_service/<congregation>/', AllUsersByService.as_view(), name='users_by_service'),
    path('users_by_leader/<congregation>/', AllUsersByLeader.as_view(), name='users_by_leader'),
    path('users_by_helper/<congregation>/', AllUsersByHelper.as_view(), name='users_by_helper'),
    path('users_by_ministry/<congregation>/', AllUsersByMinistry.as_view(), name='users_by_ministry'),
    path('users_by_groupe/<congregation>/<groupe>/', AllUsersByGroupe.as_view(), name='users_by_groupe'),
    path('set_user_groupe/<pk>/', SetGroupeView.as_view(), name='set_user_groupe'),
]