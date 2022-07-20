# Generated by Django 2.1.5 on 2020-03-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='indexed',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='position',
            field=models.IntegerField(blank=True, default=10000, null=True),
        ),
    ]
