from django.contrib import admin

from .models import Company, CompanyCategory, CompanyService, CompanyInformation, CompanyImage

import datetime
from dateutil.relativedelta import relativedelta


def add_subscription_action(modeladmin, request, queryset):
    for ele in queryset:
        ele.subscription_ends = ele.subscription_ends +  relativedelta(months=1)
        ele.save()


class CompanyImageInline(admin.TabularInline):
    model = CompanyImage


class CompanyInfoInline(admin.TabularInline):
    model = CompanyInformation
    fieldsets = (
        ('images', {
            'fields': (
                ('logo_image', 'background_image', 'small_image', ),
            )
        }),
        ('Info', {
            'fields': (
                ('address', 'phone', 'cellphone', 'website', 'email'),

            )
        }),
        ('rest', {
            'fields': (
                'description',
                ('facebook_url', 'instagram_url',)
            )
        }),

    )



@admin.register(CompanyCategory)
class CompanyCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    list_filter = ['parent', ]
    list_select_related = ['parent', ]


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'is_primary']
    list_filter = ['company', 'is_primary']
    search_fields = ['title', 'company']


@admin.register(CompanyInformation)
class CompanyInformation(admin.ModelAdmin):
    list_filter = ['company']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['status', 'business_type', 'featured', 'priority', 'category']
    list_display = ['title', 'subscription_ends', 'priority', 'max_items', 'owner', 'featured', 'status']
    readonly_fields = ['item_support', 'status', 'counter']
    list_editable = ['subscription_ends', ]
    search_fields = ['title', ]
    inlines = [CompanyImageInline, ]
    actions = [add_subscription_action, ]
    fieldsets = (
        ('Active and Subs', {
            'fields': (
                ('status',  'item_support', 'first_choice', 'featured',),
                ('business_type', 'subscription_ends', 'priority',  'max_items'),
            )
        }),
        ('Info', {
            'fields': (
                ('title',),
                ('city', 'owner', ),
                ('category', )
            )
        }),
        ('Page Detail', {
            'fields': (
                ('service_title', 'google_map_location'),
            )
        }),
        ('rest', {
            'fields': (
                ('counter', 'slug')
            )
        }),


    )

