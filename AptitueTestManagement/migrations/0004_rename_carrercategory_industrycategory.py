# Generated by Django 3.2.7 on 2021-11-15 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0003_auto_20211115_1314'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarrerCategory',
            new_name='IndustryCategory',
        ),
    ]