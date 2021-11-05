# Generated by Django 3.2.8 on 2021-10-31 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesscontact',
            name='afm',
            field=models.CharField(max_length=10, unique=True, verbose_name='ΑΦΜ'),
        ),
        migrations.AlterField(
            model_name='businesscontact',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]