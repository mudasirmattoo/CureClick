# Generated by Django 5.1.4 on 2024-12-19 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_timeslot_created_by_alter_timeslot_doctor_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='date',
            new_name='appointment_date',
        ),
    ]
