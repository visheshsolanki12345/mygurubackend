# Generated by Django 3.2.7 on 2021-12-16 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_12th', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Interpretation_10th',
            new_name='Interpretation_12th',
        ),
        migrations.AddField(
            model_name='definedgrate',
            name='P_11',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedgrate',
            name='P_12',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedgrate',
            name='P_13',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedgrate',
            name='P_14',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='definedgrate',
            name='P_15',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]