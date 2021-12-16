# Generated by Django 3.2.7 on 2021-11-27 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0016_auto_20211127_1030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='definedtestgrate',
            old_name='definedValueto',
            new_name='definedValueTo',
        ),
        migrations.RemoveField(
            model_name='definedtestgrate',
            name='grade',
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='eight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='fhour',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='five',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='nine',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='one',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='seven',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='six',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='ten',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='three',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedtestgrate',
            name='two',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]