# Generated by Django 3.2.7 on 2021-12-08 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_6To9', '0004_showgrade'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='ans1',
            new_name='a',
        ),
        migrations.RenameField(
            model_name='questions',
            old_name='ans2',
            new_name='b',
        ),
        migrations.RenameField(
            model_name='questions',
            old_name='ans3',
            new_name='c',
        ),
        migrations.RenameField(
            model_name='questions',
            old_name='ans4',
            new_name='d',
        ),
        migrations.RenameField(
            model_name='questions',
            old_name='ans5',
            new_name='e',
        ),
        migrations.AlterField(
            model_name='questions',
            name='question',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
