# Generated by Django 3.2.7 on 2022-03-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0041_alter_imageoptionstest_questiontext'),
    ]

    operations = [
        migrations.AddField(
            model_name='resulttitle',
            name='pointDiscription',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resulttitle',
            name='point',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
