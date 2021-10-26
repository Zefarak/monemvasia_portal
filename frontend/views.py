from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from companies.models import Company, CompanyCategory, City, BUSINESS_TYPE, CompanyInformation, CompanyItems
from jobPostings.models import JobPost

from companies.forms import FrontEndCompanyInformationForm, CompanyServiceForm, CompanyItemForm
from companies.models import CompanyCategory


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['page_title'] = 'Αρχική Σελίδα'
        context['page_description'] = 'Καλώς ήρθατε στο monemvasia.org. Εδώ θα βρείτε πληροφορίες για τις τοπικές ' \
                                      'επιχειρήσεις και προϊόντα.'
        context['cities'] = City.objects.filter(active=True)
        context['featured'] = Company.my_query.featured()[:6]
        context['main_companies'] = Company.my_query.first_priority()[:10]
        context['featured_jobs'] = JobPost.my_query.featured()[:5] if JobPost.my_query.featured().exists() else None

        return context


class CompanyDetailView(DetailView):
    model = Company
    queryset = Company.my_query.active()
    template_name = 'detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['detail'] = self.object.detail
        context['back_url'] = HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        context['page_title'] = f'{self.object}'
        return context


class CategoryListView(ListView):
    model = Company
    template_name = 'list_view.html'
    paginate_by = 32

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(CompanyCategory, slug=slug)
        self.category = category
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.model.objects.filter(category=self.category)
        return self.model.filter_data(self.request, qs)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['my_categories'] = CompanyCategory.objects.filter(parent=self.category)
        context['category'] = self.category
        context['page_title'] = f'{self.category}'
        context['page_description'] = f'Καλώς ήρθατε στο monemvasia.org. Επισκευτείτε την κατηγορια {self.category} ' \
                                      f'και δείτε τις τοπικές επιχειρήσεις'
        return context


class CityListView(ListView):
    template_name = 'city_list_view.html'
    model = City
    queryset = City.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(CityListView, self).get_context_data(**kwargs)
        context['page_title'] = 'ΠΕΡΙΟΧΕΣ'
        return context


class CityDetailView(ListView):
    template_name = 'city_detail_view.html'
    model = Company

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(City, slug=slug)
        self.city = category
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.filter_data(self.request, self.city.company_set.all())

    def get_context_data(self, **kwargs):
        context = super(CityDetailView, self).get_context_data(**kwargs)
        context['company_categories'] = BUSINESS_TYPE
        return context


class SearchPageView(ListView):
    model = Company
    template_name = 'list_view.html'
    paginate_by = 32

    def get_queryset(self):
        return self.model.filter_data(self.request, self.model.objects.all())


class ProductCategoryView(ListView):
    template_name = 'category_list_view.html'
    model = CompanyCategory

    def get_queryset(self):
        qs = CompanyCategory.objects.filter(parent__isnull=True)
        return qs


class ProductCategoryListView(ListView):
    template_name = 'productListView.html'
    model = ''


class ArticleDetailView(DetailView):
    model = Company
    template_name = 'detail_view.html'
    queryset = Company.objects.all()


class ContactView(FormView):
    pass


@login_required
def edit_company_page(request, slug):
    user = request.user
    obj = get_object_or_404(Company, slug=slug)
    if obj.owner != user:
        messages.warning(request, 'Η ΣΥΓΚΕΚΡΙΜΕΝΗ ΣΕΛΙΔΑ ΔΕ ΣΑΣ ΑΝΗΚΕΙ')

    form = FrontEndCompanyInformationForm(request.POST or None, instance=obj.detail)
    service_form = CompanyServiceForm(request.POST or None, initial={'company': obj})
    item_form = CompanyItemForm(request.POST or None, initial={'company': obj})

    return render(request, 'edit_customer_page.html', context={
        'form': form,
        'obj': obj,
        'service_form': service_form,
        'item_form': item_form,
        'detail': obj.detail,
        'object': obj
    })


def link_page_view(request, slug):
    company = get_object_or_404(Company, slug=slug)
    link_categories = company.instagramcategories_set.all()

    return render(request, 'link_page.html', context={
        'company': company,
        'link_categories': link_categories
    })