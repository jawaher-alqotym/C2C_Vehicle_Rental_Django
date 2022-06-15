# Generated by Django 4.0.4 on 2022-06-15 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
        ('c2c_vehicle_rental_app', '0002_alter_booking_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner_Booking', to='users_app.usercredential'),
            preserve_default=False,
        ),
    ]