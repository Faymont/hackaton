# Generated by Django 2.0 on 2019-07-27 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('for_people', '0003_ticket_is_passed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='is_passed',
            field=models.BooleanField(default=False, verbose_name='Пройден'),
        ),
    ]
