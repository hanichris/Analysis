# Generated by Django 5.0.6 on 2024-06-13 21:45

import django.core.serializers.json
import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('people', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Geofield',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('geometry', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]