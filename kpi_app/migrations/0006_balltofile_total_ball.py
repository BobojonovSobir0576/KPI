# Generated by Django 4.2.1 on 2023-06-07 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0005_userfileuplaod_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='balltofile',
            name='total_ball',
            field=models.IntegerField(default=0),
        ),
    ]
