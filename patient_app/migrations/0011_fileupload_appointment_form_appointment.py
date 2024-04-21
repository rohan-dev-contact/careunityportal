# Generated by Django 4.2.10 on 2024-04-16 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient_app', '0010_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment_form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_app.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appid', models.AutoField(primary_key=True, serialize=False)),
                ('appmadeon', models.DateField(auto_now_add=True, verbose_name='Appointment Made Date')),
                ('appdate', models.DateField(verbose_name='Appointment Date')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient_app.doctor', verbose_name='Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Patient', to='patient_app.patient')),
            ],
        ),
    ]
