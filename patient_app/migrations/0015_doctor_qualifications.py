# Generated by Django 4.1.13 on 2024-04-22 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0014_qualification_delete_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='qualifications',
            field=models.ManyToManyField(to='patient_app.qualification'),
        ),
    ]
