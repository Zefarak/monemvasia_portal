# Generated by Django 3.2.10 on 2022-03-03 05:23

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='my_adds/%Y/%m/%d/')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('category', models.CharField(choices=[('a', 'Navbar Ads. Image size 728*90'), ('b', 'Main Ads'), ('c', 'Page Ads'), ('d', 'Category Ads')], default='a', max_length=1)),
                ('url', models.URLField(blank=True)),
                ('url_blank', models.BooleanField(default=False)),
                ('text', tinymce.models.HTMLField(blank=True)),
                ('count', models.IntegerField(default=0)),
                ('article_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_add', to='articles.articlecategory')),
            ],
        ),
    ]
