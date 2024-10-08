# Generated by Django 5.1 on 2024-09-30 00:29

import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_alter_subscription_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='geofield',
            name='unique_id',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.functions.text.Concat('user', models.Value(','), 'feature_id'), output_field=models.TextField(), unique=True, verbose_name='Unique Feature ID'),
        ),
        migrations.AlterField(
            model_name='geofield',
            name='feature_id',
            field=models.TextField(),
        ),
    ]
