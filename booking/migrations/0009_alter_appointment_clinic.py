# Generated by Django 5.1.4 on 2024-12-15 17:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_appointment_clinic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.clinic'),
        ),
    ]