# Generated by Django 3.2.7 on 2021-12-28 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0006_interpretation_the_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='carrer',
            field=models.ForeignKey(blank=True, max_length=500, null=True, on_delete=django.db.models.deletion.CASCADE, to='MultipalTestAdd.career'),
        ),
    ]