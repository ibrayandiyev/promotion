# Generated by Django 2.2.6 on 2020-03-12 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20200313_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='flag',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
