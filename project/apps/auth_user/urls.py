from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter
from .views import  UserLogin, UserLogout, UserRegister



urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('register/', UserRegister.as_view()),
    path('browsable-api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = urlpatterns
