# Generated by Django 4.1.13 on 2024-04-22 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0013_remove_appointment_doctor_remove_appointment_patient_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='FileUpload',
        ),
    ]
