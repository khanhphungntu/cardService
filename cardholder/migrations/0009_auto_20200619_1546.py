# Generated by Django 3.0.7 on 2020-06-19 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cardholder', '0008_auto_20200619_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardholdermodel',
            old_name='private_key',
            new_name='token',
        ),
    ]
