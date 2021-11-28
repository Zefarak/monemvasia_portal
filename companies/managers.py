from django.db import models


class CompanyManager(models.Manager):

    def active(self):
        return self.filter(status=True)

    def normal_companies(self):
        return self.active().filter(featured=False)

    def featured(self):
        return self.active().filter(featured=True)

    def first_priority(self):
        return self.active().filter(priority='1')

    def first_choice(self):
        return self.active().filter(first_choice=True)

    def filter_data(self, request, slug=None):
        q = request.GET.get('q', None)
        city_name = request.GET.getlist('city_name', None)
        category_name = request.GET.getlist('category_name', None)
        qs = self.active().filter(category__slug=slug) if slug else self.active()
        qs = qs.filter(category__in=category_name) if category_name else qs
        qs = qs.filter(city__id__in=city_name) if city_name else qs

        if q:
            qs = qs.filter(title__search=q)

        return qs


class ServiceManager(models.Manager):

    def subscribed(self):
        return self.filter(subscribe=True)

    def active(self):
        return self.filter(active=True)

    def is_primary(self):
        return self.filter(is_primary=True)


    def filter_data(self, request):
        q = request.GET.get('q', None)
        qs = self.active()
        if q:
            qs = qs.filter(title__icontains=q)

        return qs