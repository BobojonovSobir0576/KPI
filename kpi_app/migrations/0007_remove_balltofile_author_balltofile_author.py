# Generated by Django 4.2.1 on 2023-06-07 15:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0006_balltofile_total_ball'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balltofile',
            name='author',
        ),
        migrations.AddField(
            model_name='balltofile',
            name='author',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Avtor'),
        ),
    ]
