# Generated by Django 3.2.7 on 2021-12-14 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Test_10', '0006_generalinformation_10th'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interpretation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(blank=True, max_length=200, null=True)),
                ('interpretationTitle', models.TextField(blank=True, null=True)),
                ('YouCanDoPoint_1', models.CharField(blank=True, max_length=200, null=True)),
                ('YouCanDoPoint_2', models.CharField(blank=True, max_length=200, null=True)),
                ('YouCanDoPoint_3', models.CharField(blank=True, max_length=200, null=True)),
                ('YouCanDoPoint_4', models.CharField(blank=True, max_length=200, null=True)),
                ('YouCanDoPoint_5', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
