# Generated by Django 2.0 on 2019-07-27 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('for_people', '0002_auto_20190727_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_passed',
            field=models.BooleanField(default=False),
        ),
    ]
