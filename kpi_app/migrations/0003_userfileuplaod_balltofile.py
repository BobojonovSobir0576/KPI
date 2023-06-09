# Generated by Django 4.2.1 on 2023-06-07 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0002_categories_penaltypointforquestions_questions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFileUplaod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID')),
                ('files', models.FileField(upload_to='user_files')),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "Foydalanuvchi qo'shgan ma'lumotlari",
                'verbose_name_plural': "Foydalanuvchi qo'shgan ma'lumotlari",
            },
        ),
        migrations.CreateModel(
            name='BallToFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty_files', models.FileField(upload_to='penalty_file')),
                ('date', models.DateField(auto_now_add=True)),
                ('author', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('files', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpi_app.userfileuplaod')),
            ],
            options={
                'verbose_name': "Baholovchi qo'shilgan ma'lumotga ball qo'shishi",
                'verbose_name_plural': "Baholovchi qo'shilgan ma'lumotga ball qo'shishi",
            },
        ),
    ]
