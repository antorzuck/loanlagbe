# Generated by Django 4.2 on 2024-07-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='notes',
        ),
        migrations.AddField(
            model_name='document',
            name='jamin_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='jamin_mobile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='jamin_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
