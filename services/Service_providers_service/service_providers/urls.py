from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (
    ServiceCategoryList,
    ServiceCategoryDetail,
    
    
    ServiceProviderList,
    ServiceProviderDetail,
    ServiceProviderServiceList,
    )


urlpatterns = [
    path('categories/',ServiceCategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', ServiceCategoryDetail.as_view(), name='category-detail'),


    path('serviceproviders/', ServiceProviderList.as_view(), name='service-provider-list'),
    path('serviceproviders/<int:pk>/', ServiceProviderDetail.as_view(), name='service-provider-list'),
    
    path('serviceproviderservices/', ServiceProviderServiceList.as_view(), name='service-provider-service-list'),

]

