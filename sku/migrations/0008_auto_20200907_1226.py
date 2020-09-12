# Generated by Django 3.1 on 2020-09-07 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sku', '0007_testproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inbound',
            name='product',
        ),
        migrations.RemoveField(
            model_name='outbound',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='inbound_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sku.inbound'),
        ),
        migrations.AddField(
            model_name='product',
            name='outbound_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sku.outbound'),
        ),
        migrations.AddField(
            model_name='testproduct',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='exp_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sku.warehouse'),
        ),
    ]
