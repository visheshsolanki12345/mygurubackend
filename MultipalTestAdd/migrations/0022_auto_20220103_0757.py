# Generated by Django 3.2.7 on 2022-01-03 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0021_auto_20220103_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addtest',
            name='classOrCollage',
        ),
        migrations.AddField(
            model_name='newclass',
            name='classOrCollage',
            field=models.ForeignKey(blank=True, max_length=400, null=True, on_delete=django.db.models.deletion.CASCADE, to='MultipalTestAdd.selectacademic'),
        ),
    ]
