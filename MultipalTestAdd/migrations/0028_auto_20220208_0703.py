# Generated by Django 3.2.7 on 2022-02-08 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0027_auto_20220130_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageoptionstest',
            name='aText',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='bText',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='cText',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='dText',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='eText',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='rightAns',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=300, null=True),
        ),
    ]
