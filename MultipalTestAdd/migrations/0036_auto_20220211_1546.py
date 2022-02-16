# Generated by Django 3.2.7 on 2022-02-11 10:16

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('MultipalTestAdd', '0035_auto_20220210_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiveoptionstest',
            name='question',
            field=tinymce.models.HTMLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='aText',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='bText',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='cText',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='dText',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='eText',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imageoptionstest',
            name='questionText',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interpretation',
            name='title',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='oneoptionstest',
            name='question',
            field=tinymce.models.HTMLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='optionstest',
            name='question',
            field=tinymce.models.HTMLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='resulttitle',
            name='discription',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resulttitle',
            name='point',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='threeoptionstest',
            name='question',
            field=tinymce.models.HTMLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]