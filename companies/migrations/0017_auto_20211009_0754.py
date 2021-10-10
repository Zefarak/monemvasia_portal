# Generated by Django 3.2.3 on 2021-10-09 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0016_auto_20211008_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childrens', to='companies.companycategory'),
        ),
        migrations.AlterField(
            model_name='companyitems',
            name='image',
            field=models.ImageField(help_text='400*400', upload_to='products'),
        ),
    ]