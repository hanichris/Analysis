# Generated by Django 5.1 on 2024-10-10 16:44

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_geofield_unique_id_alter_geofield_feature_id'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['id', 'email'], name='analysis_us_id_aa5374_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(condition=models.Q(('verified', True)), fields=['email'], name='unique_verified_email'),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='phonenumber',
            index=models.Index(fields=['number', 'user'], name='analysis_ph_number_2baf92_idx'),
        ),
        migrations.AddIndex(
            model_name='phonenumber',
            index=models.Index(condition=models.Q(('verified', True)), fields=['number'], name='verified_number'),
        ),
    ]