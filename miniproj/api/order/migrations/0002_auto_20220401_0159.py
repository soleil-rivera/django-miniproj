# Generated by Django 3.2.5 on 2022-04-01 01:59

from django.db import migrations, models
import miniproj.constants


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='location',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=miniproj.constants.OrderStatus['RECEIVED'], max_length=20),
        ),
    ]