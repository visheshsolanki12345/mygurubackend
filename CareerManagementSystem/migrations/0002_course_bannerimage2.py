# Generated by Django 3.2.7 on 2021-12-21 12:55

import CareerManagementSystem.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CareerManagementSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='bannerImage2',
            field=models.ImageField(blank=True, null=True, upload_to=CareerManagementSystem.models.Banner_directory_path_main),
        ),
    ]