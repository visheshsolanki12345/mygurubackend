# Generated by Django 3.2.7 on 2021-12-27 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0003_auto_20211227_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpretation',
            name='selectGrade',
            field=models.ForeignKey(blank=True, max_length=400, null=True, on_delete=django.db.models.deletion.CASCADE, to='MultipalTestAdd.interpretationgrade'),
        ),
    ]
