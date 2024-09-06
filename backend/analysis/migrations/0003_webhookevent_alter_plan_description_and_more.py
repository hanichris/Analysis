# Generated by Django 5.1 on 2024-08-28 21:17

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_report_analysis_re_id_d2677a_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookEvent',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('event_name', models.TextField()),
                ('proccessed', models.BooleanField(default=False)),
                ('proccessing_error', models.TextField()),
                ('body', models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='plan',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='plan',
            name='interval',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='plan',
            name='product_name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='plan',
            name='trial_interval',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lemonsqueezy_id', models.TextField(unique=True)),
                ('order_id', models.IntegerField()),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('status', models.TextField()),
                ('status_formatted', models.TextField()),
                ('renews_at', models.TextField()),
                ('ends_at', models.TextField()),
                ('trial_ends_at', models.TextField()),
                ('price', models.TextField()),
                ('is_usage_based', models.BooleanField(default=False)),
                ('is_paused', models.BooleanField(default=False)),
                ('subscription_item_id', models.IntegerField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]