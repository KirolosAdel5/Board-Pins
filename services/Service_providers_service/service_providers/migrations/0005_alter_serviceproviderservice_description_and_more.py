# Generated by Django 5.0.1 on 2024-02-26 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_providers', '0004_alter_serviceproviderservice_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceproviderservice',
            name='description',
            field=models.TextField(blank=True, help_text='Not Required', verbose_name='Product Description'),
        ),
        migrations.AlterField(
            model_name='sociallink',
            name='service_provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='service_providers.serviceprovider'),
            preserve_default=False,
        ),
    ]
