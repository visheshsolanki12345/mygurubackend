# Generated by Django 3.2.7 on 2021-11-27 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0020_auto_20211127_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='definedtestgrate',
            name='toFromPair',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
