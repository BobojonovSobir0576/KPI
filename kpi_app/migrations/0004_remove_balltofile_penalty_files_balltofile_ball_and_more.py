# Generated by Django 4.2.1 on 2023-06-07 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0003_userfileuplaod_balltofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balltofile',
            name='penalty_files',
        ),
        migrations.AddField(
            model_name='balltofile',
            name='ball',
            field=models.FloatField(default=0, verbose_name="Qo'yilgan ball"),
        ),
        migrations.AddField(
            model_name='balltofile',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID'),
        ),
        migrations.RemoveField(
            model_name='balltofile',
            name='author',
        ),
        migrations.AlterField(
            model_name='balltofile',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Ball'),
        ),
        migrations.AlterField(
            model_name='balltofile',
            name='files',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpi_app.userfileuplaod', verbose_name="Yuklangan faylgan ball qo'yilgan"),
        ),
        migrations.AlterField(
            model_name='userfileuplaod',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Avtor'),
        ),
        migrations.AlterField(
            model_name='userfileuplaod',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Kiritilgan sana'),
        ),
        migrations.AlterField(
            model_name='userfileuplaod',
            name='files',
            field=models.FileField(upload_to='user_files', verbose_name='Fayl'),
        ),
        migrations.CreateModel(
            name='PenaltyUplaodFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID')),
                ('ball', models.FloatField(default=0, verbose_name="Qo'yilgan ball")),
                ('files', models.FileField(upload_to='penalty_file', verbose_name='Jarima ballni isbotlash uchun Fayl yuklanganligi')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Ball')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Avtor')),
            ],
            options={
                'verbose_name': 'Jarima Ballari',
                'verbose_name_plural': 'Jarima Ballari',
            },
        ),
        migrations.AddField(
            model_name='balltofile',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Avtor'),
            preserve_default=False,
        ),
    ]
