# Generated by Django 2.2.6 on 2020-03-12 17:08

import backend.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_category_languagecampaign'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='language_campaign',
            new_name='language',
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default='0', max_digits=100)),
                ('name', models.CharField(max_length=150)),
                ('picture1', models.ImageField(blank=True, upload_to=backend.models.content_file_products_picture)),
                ('picture2', models.ImageField(blank=True, upload_to=backend.models.content_file_products_picture)),
                ('picture3', models.ImageField(blank=True, upload_to=backend.models.content_file_products_picture)),
                ('picture4', models.ImageField(blank=True, upload_to=backend.models.content_file_products_picture)),
                ('description', models.TextField(blank=True)),
                ('pdf', models.FileField(blank=True, upload_to=backend.models.content_file_product_pdf)),
                ('approved', models.BooleanField(blank=True, default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Category')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.LanguageCampaign')),
            ],
        ),
    ]