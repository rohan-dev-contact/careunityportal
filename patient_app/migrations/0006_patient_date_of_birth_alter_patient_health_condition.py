# Generated by Django 4.1.13 on 2024-03-30 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0005_specialization_remove_doctor_specialization_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='health_condition',
            field=models.TextField(),
        ),
    ]