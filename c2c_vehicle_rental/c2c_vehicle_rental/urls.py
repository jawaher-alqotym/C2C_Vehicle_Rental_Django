
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('users_app/', include('users_app.urls')),
    path('c2c_vehicle_rental_app/', include('c2c_vehicle_rental_app.urls')),
]
