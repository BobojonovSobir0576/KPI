# Generated by Django 4.2.1 on 2023-06-07 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0004_remove_balltofile_penalty_files_balltofile_ball_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfileuplaod',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kpi_app.questions', verbose_name='Qaysi savolga yuborilgani'),
            preserve_default=False,
        ),
    ]
