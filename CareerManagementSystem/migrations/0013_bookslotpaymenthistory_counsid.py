# Generated by Django 3.2.7 on 2022-02-06 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CareerManagementSystem', '0012_articlepaymenthistory_bookslotpaymenthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookslotpaymenthistory',
            name='counsId',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]