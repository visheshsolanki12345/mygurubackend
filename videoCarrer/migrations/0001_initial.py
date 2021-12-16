# Generated by Django 3.2.7 on 2021-12-16 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YouTubeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoLink', models.CharField(blank=True, max_length=300, null=True)),
                ('videoTitle', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('createAt', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
