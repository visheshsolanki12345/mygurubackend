# Generated by Django 3.2.7 on 2021-12-31 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0017_auto_20211231_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtest',
            name='createAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
