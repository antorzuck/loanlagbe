# Generated by Django 5.0.2 on 2024-06-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_customer_have_to_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='jamin_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
