# Generated by Django 5.1 on 2024-09-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_webhookevent_updated_at_alter_webhookevent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='ends_at',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='renews_at',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='trial_ends_at',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='webhookevent',
            name='proccessing_error',
            field=models.TextField(default=''),
        ),
    ]
