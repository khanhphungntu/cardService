# Generated by Django 3.0.7 on 2020-06-19 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardholder', '0006_auto_20200619_1155'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CardHolder',
        ),
        migrations.RemoveField(
            model_name='customermodel',
            name='e_commerce',
        ),
        migrations.DeleteModel(
            name='PlatformModel',
        ),
    ]
