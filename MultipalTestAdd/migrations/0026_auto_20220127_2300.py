# Generated by Django 3.2.7 on 2022-01-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0025_remove_testbackupthreequize_createat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testbackupfivequize',
            name='createAt',
        ),
        migrations.RemoveField(
            model_name='testbackupmultipalquize',
            name='createAt',
        ),
        migrations.RemoveField(
            model_name='testbackuponeimagequizecorrect',
            name='createAt',
        ),
        migrations.RemoveField(
            model_name='testbackuponequizecorrect',
            name='createAt',
        ),
        migrations.AddField(
            model_name='testbackupfivequize',
            name='number',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='testbackupmultipalquize',
            name='number',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='testbackuponeimagequizecorrect',
            name='number',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='testbackuponequizecorrect',
            name='number',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
