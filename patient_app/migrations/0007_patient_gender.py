# Generated by Django 4.1.13 on 2024-03-31 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0006_patient_date_of_birth_alter_patient_health_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]