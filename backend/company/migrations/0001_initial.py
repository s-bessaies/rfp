# Generated by Django 4.2.3 on 2024-08-29 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255)),
                ('headquarters_location', models.CharField(max_length=255)),
                ('year_established', models.IntegerField()),
                ('company_size', models.IntegerField()),
                ('revenue_last_year', models.CharField(blank=True, max_length=100)),
                ('ownership_structure', models.CharField(max_length=100)),
                ('years_of_experience', models.IntegerField()),
                ('projects', models.JSONField(default=list)),
                ('certifications', models.JSONField(default=list)),
                ('skills', models.JSONField(default=list)),
                ('it', models.JSONField(default=list)),
                ('csr_policy', models.TextField(blank=True)),
                ('environmental_commitment', models.TextField(blank=True)),
                ('sector_of_activity', models.JSONField(default=list)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
