# Generated by Django 3.2.10 on 2022-03-03 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0001_initial'),
        ('catalogue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_active', models.BooleanField(default=False, verbose_name='ΓΕΝΙΚΟΣ ΔΙΑΚΟΠΤΗΣ')),
                ('business_type', models.CharField(choices=[('1', 'ΕΜΠΟΡΙΟ'), ('2', 'ΕΣΤΙΑΣΗ'), ('3', 'ΥΠΗΡΕΣΙΕΣ'), ('4', 'ΜΕΙΚΤΟ')], default='1', max_length=1)),
                ('featured', models.BooleanField(default=False)),
                ('first_choice', models.BooleanField(default=False, verbose_name='ΠΡΟΤΕΡΙΟΤΗΤΑ')),
                ('status', models.BooleanField(default=False, verbose_name='ΚΑΤΑΣΤΑΣΗ')),
                ('subscription_ends', models.DateField(null=True)),
                ('priority', models.CharField(choices=[('1', 'ΠΛΑΝΟ ΓΙΑ ΕΠΙΧΕΙΡΗΣΕΙΣ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 50/ΜΗΝΑ'), ('2', 'ΠΛΑΝΟ ΓΙΑ ΥΠΗΡΕΣΙΕΣ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 35/ΜΗΝΑ')], default='3', max_length=1)),
                ('item_support', models.BooleanField(default=False)),
                ('max_items', models.IntegerField(default=6)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('google_map_location', models.TextField()),
                ('extra_css', models.TextField(blank=True, null=True)),
                ('service_title', models.CharField(default='ΥΠΗΡΕΣΙΕΣ', max_length=220)),
                ('counter', models.IntegerField(default=0)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΥΠΟΛΟΙΠΟ')),
            ],
            options={
                'verbose_name_plural': '1. ΕΠΙΧΕΙΡΗΣΕΙΣ',
                'ordering': ['featured', 'first_choice', 'priority'],
            },
            managers=[
                ('my_query', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('subscribe', models.BooleanField(default=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('image', models.ImageField(null=True, upload_to='companies/service/images/', verbose_name='ΕΙΚΟΝΑ')),
                ('title', models.CharField(max_length=250, verbose_name='ΤΙΤΛΟΣ')),
                ('text', models.TextField(blank=True, verbose_name='ΠΕΡΙΓΡΑΦΗ')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='ΤΙΜΗ')),
                ('counter', models.IntegerField(default=0)),
                ('slug', models.SlugField(allow_unicode=True, blank=True)),
                ('category', models.ManyToManyField(blank=True, null=True, related_name='category_services', to='catalogue.CompanyCategory')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='companies.company')),
            ],
            options={
                'verbose_name': 'ΥΠΗΡΕΣΙΑ',
                'verbose_name_plural': '4. ΥΠΗΡΕΣΙΕΣ',
            },
        ),
        migrations.CreateModel(
            name='ServiceHitCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.CharField(max_length=220)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='companies.companyservice')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='ΗΜΕΡΟΜΗΝΙΑ')),
                ('title', models.CharField(max_length=220, null=True, verbose_name='ΤΙΤΛΟΣ')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΑΞΙΑ')),
                ('payment_method', models.CharField(choices=[('a', 'ΤΡΑΠΕΖΑ ΠΕΙΡΑΙΩΣ'), ('b', 'ΕΘΝΙΚΗ ΤΡΑΠΕΖΑ'), ('c', 'ΜΕΤΡΗΤΑ')], default='a', max_length=1)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='companies.company', verbose_name='ΕΤΑΙΡΙΑ')),
            ],
            options={
                'verbose_name': 'ΠΛΗΡΩΜΗ',
                'verbose_name_plural': '1.2 ΠΛΗΡΩΜΕΣ',
            },
        ),
        migrations.CreateModel(
            name='CompanyOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='ΗΜΕΡΟΜΗΝΙΑ')),
                ('title', models.CharField(max_length=220, null=True, verbose_name='ΤΙΤΛΟΣ')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='ΑΞΙΑ')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='companies.company', verbose_name='ΕΤΑΙΡΙΑ')),
            ],
            options={
                'verbose_name': 'ΤΙΜΟΛΟΓΙΟ',
                'verbose_name_plural': '1.1 ΤΙΜΟΛΟΓΙΑ',
            },
        ),
        migrations.CreateModel(
            name='CompanyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_visible', models.BooleanField(default=True)),
                ('logo_image', models.ImageField(blank=True, help_text='lOGO ΣΤΗΝ ΣΕΛΙΔΑ ΤΟΥ ΠΕΛΑΤΗ 120*40', upload_to='companies/logos/')),
                ('logo_site', models.ImageField(blank=True, help_text='LOGO ΣΤΗΝ ΔΙΚΗ ΜΑΣ ΣΕΛΙΔΑ 400*600', null=True, upload_to='companies/logo_site/')),
                ('address', models.CharField(blank=True, max_length=220, verbose_name='ΔΙΕΥΘΥΝΣΗ')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='ΤΗΛΕΦΩΝΟ')),
                ('cellphone', models.CharField(blank=True, max_length=20, verbose_name='ΚΙΝΗΤΟ')),
                ('website', models.URLField(blank=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='ΠΕΡΙΓΡΑΦΗ')),
                ('facebook_url', models.URLField(blank=True, null=True, verbose_name='ΣΕΛΙΔΑ FACEBOOK')),
                ('instagram_url', models.URLField(blank=True, null=True, verbose_name='ΣΕΛΙΔΑ INSTAGRAM')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='companies.company')),
            ],
            options={
                'verbose_name_plural': '2. ΠΡΟΦΙΛ ΕΠΙΧΕΙΡΗΣΕΩΝ',
            },
        ),
        migrations.CreateModel(
            name='CompanyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='companies/images/')),
                ('background_img', models.BooleanField(default=False, verbose_name='ΕΞΩΦΥΛΛΟ')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='companies.company')),
            ],
            options={
                'verbose_name_plural': '2. ΕΙΚΟΝΕΣ ΕΠΙΧΕΙΡΗΣΕΩΝ',
            },
        ),
        migrations.CreateModel(
            name='CompanyHitCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.CharField(max_length=220)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hits', to='companies.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220)),
                ('image', models.ImageField(blank=True, null=True, upload_to='companies/categories/')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childrens', to='companies.companycategory')),
            ],
            options={
                'verbose_name': 'ΚΑΤΗΓΟΡΙΑ ΕΤΑΙΡΙΑΣ',
                'verbose_name_plural': '5. ΚΑΤΗΓΟΡΙΕΣ ΕΤΑΙΡΙΩΝ',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, related_name='my_companies', to='companies.CompanyCategory'),
        ),
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.city'),
        ),
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies', to=settings.AUTH_USER_MODEL),
        ),
    ]
