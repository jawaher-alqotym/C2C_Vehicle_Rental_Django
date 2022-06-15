

from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = "users_app"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

