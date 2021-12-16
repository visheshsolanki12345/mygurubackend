# Generated by Django 3.2.7 on 2021-11-27 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0015_testresult_industry_grade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='definedtestgrate',
            old_name='definedValue',
            new_name='definedValueFrom',
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='definedValueto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='industry_Grade',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
