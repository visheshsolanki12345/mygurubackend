# Generated by Django 3.2.7 on 2021-11-16 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0007_alter_questionmanagement_ans5'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionmanagement',
            name='ans5',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]