# Generated by Django 3.2.7 on 2021-12-04 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0022_showgrade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionmanagement',
            name='grade',
        ),
        migrations.AlterField(
            model_name='testschedulemanagement',
            name='grade',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]