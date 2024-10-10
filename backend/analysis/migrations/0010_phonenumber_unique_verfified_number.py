# Generated by Django 5.1 on 2024-10-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0009_phonenumber_user_verified_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='phonenumber',
            constraint=models.UniqueConstraint(condition=models.Q(('verified', True)), fields=('number', 'user'), name='unique_verfified_number'),
        ),
    ]
