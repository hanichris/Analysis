# Generated by Django 5.1 on 2024-08-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='report',
            index=models.Index(fields=['id'], name='analysis_re_id_d2677a_idx'),
        ),
    ]
