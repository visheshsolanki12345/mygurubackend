# Generated by Django 3.2.7 on 2021-12-27 06:38

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0002_rename_totalno_reports_totalnoqu'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='the_json',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='interpretation',
            name='point',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
