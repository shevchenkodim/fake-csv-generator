# Generated by Django 3.1.4 on 2020-12-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_auto_20201220_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='rows',
            field=models.IntegerField(default=0, verbose_name='Rows'),
        ),
    ]
