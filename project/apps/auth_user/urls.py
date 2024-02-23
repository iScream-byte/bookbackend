from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter
from .views import UserViewSet, UserLogin, UserLogout, UserRegister

auth_router = SimpleRouter()

auth_router.register("all-users-list",
                     UserViewSet,
                     basename="all_users")

urlpatterns = [
    path('login/', UserLogin.as_view()),
    path('logout/', UserLogout.as_view()),
    path('register/', UserRegister.as_view()),
    path('browsable-api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = urlpatterns + auth_router.urls
