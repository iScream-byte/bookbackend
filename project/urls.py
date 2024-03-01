from django.contrib import admin
from django.urls import path, include
from .apps.core.views import return_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("core.urls")),
    path('auth/', include("auth_user.urls")),
    path('media/<str:image_name>/',return_image)

]
