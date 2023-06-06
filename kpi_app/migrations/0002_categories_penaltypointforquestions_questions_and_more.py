# Generated by Django 4.2.1 on 2023-06-03 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Bosh kategoriyaga tegishli Kategoriyalar',
                'verbose_name_plural': 'Bosh kategoriyaga tegishli Kategoriyalar',
            },
        ),
        migrations.CreateModel(
            name='PenaltyPointForQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('description', models.TextField(verbose_name='Jarima ballar(asoslovchi hujjat asosida) ')),
            ],
            options={
                'verbose_name': 'Savollarning Jarima Ballari',
                'verbose_name_plural': 'Savollarning Jarima Ballari',
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Amalga oshiradigan ishlar')),
                ('date_of_calculation_ball', models.CharField(max_length=50, verbose_name='Natijalarni hisoblab borish muddati')),
                ('ball_of_question', models.IntegerField(default=0, verbose_name='Ball')),
                ('description', models.TextField(verbose_name='Ballarni hisoblash metodikasi')),
                ('categories_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpi_app.categories', verbose_name='Kategoriyaning IDsi')),
                ('penalty_id', models.ManyToManyField(to='kpi_app.penaltypointforquestions', verbose_name='Jarimalar izohi')),
            ],
            options={
                'verbose_name': 'Kategoriyaning Savollari',
                'verbose_name_plural': 'Kategoriyaning Savollari',
            },
        ),
        migrations.CreateModel(
            name='MainCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Asosiy Kategoriya')),
                ('author', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Baholovchi tanlash')),
            ],
            options={
                'verbose_name': 'Bosh kategoriya',
                'verbose_name_plural': 'Bosh kategoriya',
            },
        ),
        migrations.AddField(
            model_name='categories',
            name='main_categories_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kpi_app.maincategories', verbose_name='Asosiy Kategoriyaning IDsi'),
        ),
    ]