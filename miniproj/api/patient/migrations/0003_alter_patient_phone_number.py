# Generated by Django 3.2.5 on 2022-03-31 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patient_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]