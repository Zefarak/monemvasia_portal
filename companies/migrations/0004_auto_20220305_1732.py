# Generated by Django 3.2.8 on 2022-03-05 15:32

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20220305_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryForCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220)),
                ('image', models.ImageField(blank=True, null=True, upload_to='companies/categories/')),
                ('big_image', models.ImageField(blank=True, null=True, upload_to='companies/catalogue/upload-big-images/')),
                ('text', tinymce.models.HTMLField(blank=True, null=True)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childrens', to='companies.categoryforcompany', verbose_name='Κατηγορία')),
            ],
            options={
                'verbose_name': 'ΚΑΤΗΓΟΡΙΑ ΕΤΑΙΡΙΑΣ',
                'verbose_name_plural': '5. ΚΑΤΗΓΟΡΙΕΣ ΕΤΑΙΡΙΩΝ',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='company', to='companies.CategoryForCompany'),
        ),
    ]
