# Generated by Django 4.2.1 on 2023-06-07 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_app', '0008_remove_penaltyuplaodfile_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='penaltyuplaodfile',
            name='get_file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kpi_app.userfileuplaod', verbose_name="Yuklangan faylgan ball qo'yilgan"),
            preserve_default=False,
        ),
    ]
