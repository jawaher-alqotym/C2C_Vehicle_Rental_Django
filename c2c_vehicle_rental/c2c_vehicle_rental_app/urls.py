from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = "c2c_vehicle_rental_app"

urlpatterns = [
    path('list_vehicles/', views.list_vehicles, name='list_vehicles'),
    path('add_vehicle/', views.add_vehicle, name='add_vehicle'),
    path('update_vehicle/<vehicle_id>', views.update_vehicle, name='update_vehicle'),
    path('delete_vehicle/<vehicle_id>', views.delete_vehicle, name='delete_vehicle'),
    path('list_my_vehicles/', views.list_my_vehicles, name='list_my_vehicles'),

    path('list_reviews_about_user/<user_id>', views.list_reviews_about_user, name='list_reviews_about_user'),
    path('add_review/<user_id>', views.add_review, name='add_review'),
    path('edit_review/<review_id>', views.edit_review, name='edit_review'),
    path('delete_review/<review_id>', views.delete_review, name='delete_review'),
    path('list_my_reviews/', views.list_my_reviews, name='list_my_reviews'),

    path('create_booking/<vehicle_id>', views.create_booking, name='create_booking'),
    path('list_owner_booking/', views.list_owner_booking, name='list_owner_booking'),
    path('list_rentee_booking/', views.list_rentee_booking, name='list_rentee_booking'),
    path('approve_booking/<booking_id>', views.approve_booking, name='approve_booking'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)