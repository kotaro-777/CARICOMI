# Generated by Django 3.0.8 on 2021-01-20 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service',
            field=models.CharField(default=1, max_length=25, verbose_name='サービス名'),
        ),
    ]
