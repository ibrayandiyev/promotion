# Generated by Django 2.2.6 on 2020-03-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_product_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='flagcolor',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
