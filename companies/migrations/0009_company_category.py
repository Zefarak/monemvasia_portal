# Generated by Django 3.2.3 on 2021-10-04 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_auto_20211004_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='companies.CompanyCategory'),
        ),
    ]
