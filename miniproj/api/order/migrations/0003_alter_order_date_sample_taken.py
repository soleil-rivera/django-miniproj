# Generated by Django 3.2.5 on 2022-04-01 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20220401_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_sample_taken',
            field=models.DateTimeField(null=True),
        ),
    ]