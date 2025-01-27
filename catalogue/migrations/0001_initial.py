# Generated by Django 3.2.10 on 2022-03-03 05:23

import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=120, verbose_name='Τίτλος')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Σχόλια')),
                ('timestamp', models.DateField(auto_now=True)),
                ('meta_description', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name_plural': '3. Κατηγορίες Site',
            },
        ),
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=120, verbose_name='Τίτλος')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Σχόλια')),
                ('timestamp', models.DateField(auto_now=True)),
                ('meta_description', models.CharField(blank=True, max_length=300)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name_plural': '3. Κατηγορίες Site',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribe', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=220)),
                ('image', models.ImageField(blank=True, upload_to='company/images/')),
                ('is_offer', models.BooleanField(default=False, verbose_name='Προσφορά')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Περιγραφή')),
                ('sku', models.CharField(blank=True, max_length=150, null=True)),
                ('text', tinymce.models.HTMLField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=240, null=True)),
                ('product_url', models.URLField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Αρχική Τιμή')),
                ('price_discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Εκπτωτική Τιμή')),
                ('final_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Τιμή Πώλησης')),
                ('vector_column', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('counter', models.IntegerField(default=0)),
                ('category', models.ManyToManyField(blank=True, to='catalogue.Category', verbose_name='Κατηγορία')),
            ],
            options={
                'verbose_name_plural': 'ΠΡΟΪΟΝΤΑ',
            },
        ),
        migrations.CreateModel(
            name='ProductHitCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.CharField(max_length=220)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='catalogue.product')),
            ],
        ),
    ]
