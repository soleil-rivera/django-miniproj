# Generated by Django 3.2.5 on 2022-03-18 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.IntegerField(),
        ),
    ]
