# Generated by Django 5.0.2 on 2024-06-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_customer_profit'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='have_to_pay',
            field=models.IntegerField(default=0),
        ),
    ]
