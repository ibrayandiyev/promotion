# Generated by Django 2.2.6 on 2020-03-22 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_aboutus'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.LanguageCampaign'),
        ),
    ]