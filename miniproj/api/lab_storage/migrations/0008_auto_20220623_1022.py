# Generated by Django 3.2.5 on 2022-06-23 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_storage', '0007_alter_labstorage_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labstorage',
            name='created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='labstorage',
            name='last_updated',
            field=models.DateField(auto_now=True),
        ),
    ]
