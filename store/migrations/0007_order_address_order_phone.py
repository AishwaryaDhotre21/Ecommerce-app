# Generated by Django 4.0.3 on 2022-03-23 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, default=' ', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, default=' ', max_length=10),
        ),
    ]
