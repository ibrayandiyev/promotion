# Generated by Django 2.1.5 on 2020-03-14 11:11

import backend.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20200313_1809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('picture', models.ImageField(blank=True, upload_to=backend.models.content_file_banner_picture)),
                ('position', models.IntegerField(blank=True, default=10000, null=True)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.LanguageCampaign')),
            ],
        ),
    ]
