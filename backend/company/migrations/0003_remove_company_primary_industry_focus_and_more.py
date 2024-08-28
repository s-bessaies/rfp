# Generated by Django 4.2.3 on 2024-08-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_rename_it_infrastructure_company_it'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='primary_industry_focus',
        ),
        migrations.AddField(
            model_name='company',
            name='sector_of_activity',
            field=models.JSONField(default=dict),
        ),
    ]
