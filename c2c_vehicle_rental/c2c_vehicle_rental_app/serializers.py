
from rest_framework import serializers
from .models import *

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = ['vehicle_brand',
                  'category',
                  'year_of_making',
                  'hourly_rental_price',
                  'location']


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ['vehicle_delivery', 'start_date' , 'end_date']


class ReviwesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviwes
        fields = ['rating', 'comment']
