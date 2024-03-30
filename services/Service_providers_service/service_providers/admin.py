from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    ServiceCategory,
    ServiceProvider,
    ServiceProviderImage,
    ServiceProviderSpecification,
    ServiceProviderSpecificationValue,
    ServiceProviderType,
    Tag,
    ServiceProviderReview,
ServiceProviderService
)


class ServiceProviderSpecification(admin.TabularInline):
    model = ServiceProviderSpecification
    
@admin.register(ServiceProviderType)
class Admin(admin.ModelAdmin):
    inlines = [
        ServiceProviderSpecification 
    ]

    


class ServicesImageInline(admin.TabularInline):
    model = ServiceProviderImage

admin.site.register(ServiceCategory, MPTTModelAdmin)

class ServiceProviderSpecificationValueInline(admin.TabularInline):
    model = ServiceProviderSpecificationValue



class ProductTagsForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Tags', is_stacked=False),
        required=False  # Set required to False to make it not required

    )

    class Meta:
        model = ServiceProvider
        fields = '__all__'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ReviewInline(admin.TabularInline):
    model = ServiceProviderReview  # Include the Review model

class ServiceProviderService(admin.TabularInline):
    model = ServiceProviderService
    extra = 1
@admin.register(ServiceProvider)
class ServiceProvider(admin.ModelAdmin):
    list_display = ('title',)


    list_per_page = 20 
    
    inlines = [
        ServiceProviderSpecificationValueInline,
        ServicesImageInline,
        ReviewInline,
        ServiceProviderService
    ]
    form = ProductTagsForm
