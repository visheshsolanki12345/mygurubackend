# Generated by Django 3.2.7 on 2022-02-13 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCarrer', '0006_videopaymenthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocarrer',
            name='hide',
            field=models.BooleanField(default=False),
        ),
    ]
