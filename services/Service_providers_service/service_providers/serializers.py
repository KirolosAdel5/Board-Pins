from rest_framework import serializers
from .models import ServiceCategory, ServiceProviderType, ServiceProviderSpecification, ServiceProvider, Tag, ServiceProviderSpecificationValue, ServiceProviderImage, ServiceProviderReview, SocialLink, ServiceProviderService
from rest_framework_recursive.fields import RecursiveField

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'parent', 'slug','is_active']


class ServiceProviderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderType
        fields = '__all__'

class ServiceProviderSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderSpecification
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ServiceProviderSpecificationValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderSpecificationValue
        fields = '__all__'

class ServiceProviderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderImage
        fields = '__all__'

class ServiceProviderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderReview
        fields = '__all__'

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'

class ServiceProviderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderService
        fields = '__all__'
        
class ServiceProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceProvider
        fields = '__all__'

