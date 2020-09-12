# Generated by Django 3.1 on 2020-09-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sku', '0012_auto_20200907_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplace',
            name='code',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='code',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='code',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
