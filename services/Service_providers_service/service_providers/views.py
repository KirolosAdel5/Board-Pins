from rest_framework import generics,viewsets
from .models import ServiceCategory, ServiceProviderType, ServiceProviderSpecification, ServiceProvider, Tag, ServiceProviderSpecificationValue, ServiceProviderImage, ServiceProviderReview, SocialLink, ServiceProviderService
from .serializers import ServiceCategorySerializer, ServiceProviderTypeSerializer, ServiceProviderSpecificationSerializer, ServiceProviderSerializer, TagSerializer, ServiceProviderSpecificationValueSerializer, ServiceProviderImageSerializer, ServiceProviderReviewSerializer, SocialLinkSerializer, ServiceProviderServiceSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
import requests
from .permissions import IsStaffOrReadOnly, IsStaff,IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
 
class ServiceCategoryList(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes  = [IsAuthenticated,IsStaffOrReadOnly]

class ServiceCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes  = [IsStaff]

   
class ServiceProviderList(generics.ListCreateAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    

class ServiceProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    
class ServiceProviderServiceList(generics.ListAPIView):
    queryset = ServiceProviderService.objects.all()
    serializer_class = ServiceProviderServiceSerializer