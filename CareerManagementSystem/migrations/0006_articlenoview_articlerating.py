# Generated by Django 3.2.7 on 2022-02-03 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CareerManagementSystem', '0005_auto_20220203_2128'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, default=0, null=True)),
                ('editorApproveArticle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CareerManagementSystem.editorapprovearticle')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleNoView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipAddress', models.CharField(blank=True, max_length=400, null=True)),
                ('noView', models.IntegerField(blank=True, default=0, null=True)),
                ('editorApproveArticle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CareerManagementSystem.editorapprovearticle')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
