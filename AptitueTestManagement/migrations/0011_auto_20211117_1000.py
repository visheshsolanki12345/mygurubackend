# Generated by Django 3.2.7 on 2021-11-17 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AptitueTestManagement', '0010_alter_testresult_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='totalCount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='ans1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='ans2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='ans3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='ans4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='ans5',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='industry',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]