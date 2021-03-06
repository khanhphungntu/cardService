# Generated by Django 3.0.7 on 2020-06-19 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cardholder', '0004_auto_20200618_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('private_key', models.CharField(max_length=255, unique=True)),
                ('public_key', models.CharField(max_length=255, unique=True)),
                ('e_commerce_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardholder.PlatformModel')),
            ],
        ),
    ]
