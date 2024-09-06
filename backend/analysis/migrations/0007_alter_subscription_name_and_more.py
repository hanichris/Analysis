# Generated by Django 5.1 on 2024-09-06 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_rename_proccessed_webhookevent_processed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['lemonsqueezy_id'], name='analysis_su_lemonsq_c91dcc_idx'),
        ),
    ]
