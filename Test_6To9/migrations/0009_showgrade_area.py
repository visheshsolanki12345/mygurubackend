# Generated by Django 3.2.7 on 2021-12-15 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_6To9', '0008_auto_20211215_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='showgrade',
            name='area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]