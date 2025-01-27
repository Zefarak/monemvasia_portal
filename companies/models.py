from django.db import models
from django.db.models import Q, Sum
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

import datetime
from tinymce.models import HTMLField
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField

from .managers import CompanyManager, ServiceManager
from frontend.models import City


User = get_user_model()

BUSINESS_TYPE = (
        ('1', 'ΕΜΠΟΡΙΟ'),
        ('2', 'ΕΣΤΙΑΣΗ'),
        ('3', 'ΥΠΗΡΕΣΙΕΣ'),
        ('4', 'ΜΕΙΚΤΟ')
    )


def upload_to(instance, filename):
    return f'/companies/images/{instance.id}/{filename}'


def upload_image(instance, filename):
    return f'/companies/images/{instance.company.id}/{filename}'


def upload_logo(instance, filename):
    return f'/companies/logos/{instance.company.id}/{filename}'


def upload_services(instance, filename):
    return f'/companies/services/{instance.company.id}/{filename}'


PAYMENT_METHODS = [
    ('a', 'ΤΡΑΠΕΖΑ ΠΕΙΡΑΙΩΣ'),
    ('b', 'ΕΘΝΙΚΗ ΤΡΑΠΕΖΑ'),
    ('c', 'ΜΕΤΡΗΤΑ'),
]

PRIORITY_OPTIONS = (
        ('1', 'ΠΛΑΝΟ ΓΙΑ ΕΠΙΧΕΙΡΗΣΕΙΣ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 50/ΜΗΝΑ'),
        ('2', 'ΠΛΑΝΟ ΓΙΑ ΥΠΗΡΕΣΙΕΣ: ΚΟΣΤΟΣ ΣΥΝΔΡΟΜΗΣ 35/ΜΗΝΑ'),
    )


class CategoryForCompany(MPTTModel):
    name = models.CharField(max_length=220)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='childrens', verbose_name='Κατηγορία')
    image = models.ImageField(upload_to='companies/categories/', blank=True, null=True)
    big_image = models.ImageField(upload_to='companies/catalogue/upload-big-images/', blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    class Meta:
        verbose_name_plural = '5. ΚΑΤΗΓΟΡΙΕΣ ΕΤΑΙΡΙΩΝ'
        verbose_name = 'ΚΑΤΗΓΟΡΙΑ ΕΤΑΙΡΙΑΣ'

    def front_name(self):
        full_path = [f'- {self.name}']
        k = self.parent
        while k is not None:
            space_sym = "&nbsp" * 4
            full_path.append(space_sym)
            k = k.parent
        return ''.join(full_path[::-1])

    def is_parent(self):
        return False if self.childrens.exists() else True

    def get_absolute_url(self):
        return reverse('product_category', kwargs={'slug': self.slug})

    def get_childrens(self):
        childrens = self.childrens.filter(active=True).order_by('order')
        return childrens


class CompanyCategory(models.Model):
    title = models.CharField(max_length=220)
    image = models.ImageField(upload_to='companies/categories/', blank=True, null=True)
    big_image = models.ImageField(upload_to='companies/catalogue/upload-big-images/', blank=True, null=True)
    text = HTMLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='childrens')

    class Meta:
        verbose_name_plural = '5. ΚΑΤΗΓΟΡΙΕΣ ΕΤΑΙΡΙΩΝ'
        verbose_name = 'ΚΑΤΗΓΟΡΙΑ ΕΤΑΙΡΙΑΣ'


    def __str__(self):
        return self.title

    def is_parent(self):
        return True if self.have_childrens() else False

    def get_absolute_url(self):
        if self.is_parent():
            return reverse('category_parent_list_view', kwargs={'slug': self.slug})
        else:
            return reverse('category', kwargs={'slug': self.slug})

    def have_childrens(self):
        return self.childrens.exists()

    def tag_image(self):
        return self.image.url if self.image else ''

    def tag_big_image(self):
        return self.big_image.url if self.big_image else ''


class Company(models.Model):
    admin_active = models.BooleanField(default=False, verbose_name='ΓΕΝΙΚΟΣ ΔΙΑΚΟΠΤΗΣ')
    business_type = models.CharField(choices=BUSINESS_TYPE, default='1', max_length=1)
    featured = models.BooleanField(default=False)
    first_choice = models.BooleanField(default=False, verbose_name='ΠΡΟΤΕΡΙΟΤΗΤΑ')
    category = models.ManyToManyField(CompanyCategory, null=True, blank=True, related_name='my_companies')
    categories = models.ManyToManyField(CategoryForCompany, null=True, blank=True, related_name='company')
    status = models.BooleanField(default=False, verbose_name='ΚΑΤΑΣΤΑΣΗ')
    subscription_ends = models.DateField(null=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default='3')
    item_support = models.BooleanField(default=False)
    max_items = models.IntegerField(default=6)
    title = models.CharField(max_length=200)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='companies')
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    google_map_location = models.TextField()
    extra_css = models.TextField(null=True, blank=True)

    # page_relates_fields
    service_title = models.CharField(max_length=220, default='ΥΠΗΡΕΣΙΕΣ')

    my_query = CompanyManager()
    objects = models.Manager()

    counter = models.IntegerField(default=0)
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0, verbose_name='ΥΠΟΛΟΙΠΟ')

    class Meta:
        ordering = ['featured', 'first_choice', 'priority',]
        verbose_name_plural = '1. ΕΠΙΧΕΙΡΗΣΕΙΣ'
        
    def save(self, *args, **kwargs):
        if self.admin_active:
            self.status = True if self.subscription_ends >= datetime.datetime.now().date() else False
        else:
            self.status = False
        self.item_support = True if self.max_items > 0 else False
        orders = self.orders.aggregate(Sum('value'))['value__sum'] if self.orders.exists() else 0
        payments = self.payments.aggregate(Sum('value'))['value__sum'] if self.payments.exists() else 0
        self.value = orders - payments
        self.counter = self.hits.count()
        super(Company, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('company_view', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('accounts:update_company_info', kwargs={'slug': self.slug})

    def support_products(self):
        return True if self.business_type in ['1', '4'] else False

    def support_service(self)-> bool:
        return True if self.business_type in ['3', '4'] else False

    def sub_value(self):
        return 20 if self.business_type == '3' else 40 if self.business_type == '2' else 100

    def get_background_image(self):
        qs = self.images.filter(background_img=True)
        return qs.first().image.url if qs.exists() else None

    def rest_photos(self):
        return self.images.filter(background_img=False)

    @staticmethod
    def filter_data(request, qs):
        q = request.GET.get('q', None)
        if q:
            qs = qs.filter(Q(title__icontains=q) |
                           Q(city__title__icontains=q)
                           )
        return qs


class CompanyHitCounter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='hits')
    session = models.CharField(max_length=220)

    def save(self, *args, **kwargs):
        super(CompanyHitCounter, self).save(*args, **kwargs)
        self.company.save()

    def __str__(self):
        return self.company

    @staticmethod
    def update_hit(request, company):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        session = request.session.session_key
        qs = CompanyHitCounter.objects.filter(company=company, session=session)
        if qs.exists():
            last_obj = qs.last()
            diff = datetime.datetime.today() - last_obj.timestamp.replace(tzinfo=None)
            if diff.days > 1:
                CompanyHitCounter.objects.create(
                    company=company,
                    session=session
                )
        else:
            CompanyHitCounter.objects.create(
                company=company,
                session=session
            )


class CompanyInformation(models.Model):
    is_visible = models.BooleanField(default=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='detail')
    logo_image = models.ImageField(blank=True, upload_to='companies/logos/', help_text='lOGO ΣΤΗΝ ΣΕΛΙΔΑ ΤΟΥ ΠΕΛΑΤΗ 120*40')
    logo_site = models.ImageField(blank=True, null=True, upload_to='companies/logo_site/', help_text='LOGO ΣΤΗΝ ΔΙΚΗ ΜΑΣ ΣΕΛΙΔΑ 400*600')
    address = models.CharField(blank=True, verbose_name='ΔΙΕΥΘΥΝΣΗ', max_length=220)
    phone = models.CharField(max_length=20, blank=True, verbose_name='ΤΗΛΕΦΩΝΟ')
    cellphone = models.CharField(max_length=20, blank=True, verbose_name='ΚΙΝΗΤΟ')
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True, null=True)
    description = HTMLField(blank=True, null=True, verbose_name='ΠΕΡΙΓΡΑΦΗ')
    facebook_url = models.URLField(blank=True, null=True, verbose_name='ΣΕΛΙΔΑ FACEBOOK')
    instagram_url = models.URLField(blank=True, null=True, verbose_name='ΣΕΛΙΔΑ INSTAGRAM')

    class Meta:
        verbose_name_plural = '2. ΠΡΟΦΙΛ ΕΠΙΧΕΙΡΗΣΕΩΝ'

    def __str__(self):
        return self.company.title

    def full_phones(self):
        phones = self.cellphone if self.cellphone else ''
        phones += f' | {self.phone}' if self.phone else '.'
        return phones

    def full_address(self):
        return f'{self.address} | {self.company.city}'

    def tag_image(self):
        return self.logo_site.url if self.logo_site else ' '

    def tag_logo(self):
        return self.logo_image.url if self.logo_image else ' '

    def show_products(self):
        return True if self.company.business_type in ['1', '4'] else False

    def show_services(self):
        return True if self.company.business_type in ['2', '3'] else False


class CompanyImage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='companies/images/')
    background_img = models.BooleanField(default=False, verbose_name='ΕΞΩΦΥΛΛΟ')

    class Meta:
        verbose_name_plural = '2. ΕΙΚΟΝΕΣ ΕΠΙΧΕΙΡΗΣΕΩΝ'

    def get_edit_url(self):
        return reverse('accounts:update_company_image', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('accounts:delete_company_image', kwargs={'pk': self.pk})


class ServiceCategory(MPTTModel):
    is_featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=120, verbose_name='Τίτλος')

    content = models.TextField(blank=True, null=True, verbose_name='Σχόλια')
    timestamp = models.DateField(auto_now=True)
    meta_description = models.CharField(max_length=300, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Κατηγορία')

    slug = models.SlugField(blank=True, null=True, allow_unicode=True)

    objects = models.Manager()

    class Meta:
        app_label = 'catalogue'
        verbose_name_plural = '1. Κατηγορίες Service'

    def save(self, *args, **kwargs):
        new_slug = slugify(self.name, allow_unicode=True)
        qs_exists = ServiceCategory.objects.filter(slug=new_slug)
        self.slug = f'{new_slug}-{self.id}' if qs_exists.exists() else new_slug
        super().save()

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def front_name(self):
        full_path = [f'- {self.name}']
        k = self.parent
        while k is not None:
            space_sym = "&nbsp" * 4
            full_path.append(space_sym)
            k = k.parent
        return ''.join(full_path[::-1])

    def tag_active(self):
        return 'Is Active' if self.active else 'No active'

    def is_parent(self):
        return False if self.category_services.exists() else True

    def get_absolute_url(self):
        return reverse('product_category', kwargs={'slug': self.slug})

    def get_childrens(self):
        childrens = self.children.filter(active=True).order_by('order')
        return childrens



class CompanyService(models.Model):
    active = models.BooleanField(default=True)
    subscribe = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to='companies/service/images/', verbose_name='ΕΙΚΟΝΑ', null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=250, verbose_name='ΤΙΤΛΟΣ')
    text = models.TextField(verbose_name='ΠΕΡΙΓΡΑΦΗ', blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='ΤΙΜΗ')
    counter = models.IntegerField(default=0)
    objects = models.Manager()
    slug = models.SlugField(blank=True, allow_unicode=True)
    category = models.ManyToManyField(ServiceCategory, blank=True, null=True, related_name='category_services')
    my_query = ServiceManager()

    class Meta:
        verbose_name_plural = '4. ΥΠΗΡΕΣΙΕΣ'
        verbose_name = 'ΥΠΗΡΕΣΙΑ'

    def save(self, *args, **kwargs):
        self.subscribe = self.company.status
        self.counter = self.hits.all().count()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('company:service_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('company:service-delete', kwargs={'pk': self.id})

    def tag_primary(self):
        return 'ΕΧΕΙ ΠΡΟΤΕΡΙΟΤΗΤΑ' if self.is_primary else 'ΔΕ ΕΧΕΙ'

    def tag_image(self):
        return self.image.url if self.image else ''

    def get_detail_url(self):
        return reverse('company_view', kwargs={'slug': self.company.slug})

    @staticmethod
    def filter_data(request, qs):
        q = request.GET.get('q', None)
        qs = qs.filter(title__icontains=q) if q else qs
        return qs


class ServiceHitCounter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(CompanyService, on_delete=models.CASCADE, related_name='hits')
    session = models.CharField(max_length=220)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.service.save()

    def __str__(self):
        return self.service

    @staticmethod
    def update_hit(request, service):
        if not request.session.exists(request.session.session_key):
            request.session.create()
        session = request.session.session_key
        qs = ServiceHitCounter.objects.filter(service=service, session=session)
        if qs.exists():
            last_obj = qs.last()
            diff = datetime.datetime.today() - last_obj.timestamp.replace(tzinfo=None)
            if diff.days > 1:
                ServiceHitCounter.objects.create(
                    service=service,
                    session=session
                )
        else:
            ServiceHitCounter.objects.create(
                service=service,
                session=session
            )


class CompanyPayment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payments', verbose_name='ΕΤΑΙΡΙΑ')
    date = models.DateField(verbose_name='ΗΜΕΡΟΜΗΝΙΑ')
    title = models.CharField(null=True, max_length=220, verbose_name='ΤΙΤΛΟΣ')
    value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='ΑΞΙΑ')
    payment_method = models.CharField(max_length=1, default='a', choices=PAYMENT_METHODS)

    def save(self, *args, **kwargs):
        super(CompanyPayment, self).save(*args, **kwargs)
        self.company.save()

    class Meta:
        verbose_name_plural = '1.2 ΠΛΗΡΩΜΕΣ'
        verbose_name = 'ΠΛΗΡΩΜΗ'

    def __str__(self):
        return f'{self.company} | {self.date}'


class CompanyOrder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders', verbose_name='ΕΤΑΙΡΙΑ')
    date = models.DateField(verbose_name='ΗΜΕΡΟΜΗΝΙΑ')
    title = models.CharField(null=True, max_length=220, verbose_name='ΤΙΤΛΟΣ')
    value = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='ΑΞΙΑ')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.company.save()

    class Meta:
        verbose_name_plural = '1.1 ΤΙΜΟΛΟΓΙΑ'
        verbose_name = 'ΤΙΜΟΛΟΓΙΟ'

    def __str__(self):
        return f'{self.company} | {self.date}'




