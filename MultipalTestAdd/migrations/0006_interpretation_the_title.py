# Generated by Django 3.2.7 on 2021-12-28 08:08

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0005_auto_20211227_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='the_title',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
