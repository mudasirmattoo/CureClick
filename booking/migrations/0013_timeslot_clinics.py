# Generated by Django 5.1.4 on 2024-12-23 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_rename_date_timeslot_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='clinics',
            field=models.ManyToManyField(blank=True, to='booking.clinic'),
        ),
    ]