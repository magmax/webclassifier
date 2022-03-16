# Generated by Django 4.0.3 on 2022-03-16 04:19

import classifier.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0002_rename_binaries_binary_alter_binary_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='status',
            field=models.CharField(choices=[('unprocessed', 'UNPROCESSED'), ('unknown', 'UNKNOWN'), ('error', 'ERROR'), ('spam', 'SPAM'), ('jam', 'JAM')], default=classifier.models.Status['UNPROCESSED'], max_length=12),
        ),
    ]