from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Avg
import uuid

class ServiceCategory(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(unique=True,verbose_name=_("Category safe URL"), max_length=255)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Service Categories")

    def get_absolute_url(self):
        return reverse("service_providers:category_list", args=[self.slug])

    def __str__(self):
        return self.name
    def get_parent(self):
        try:
            # Assuming there's a ForeignKey field named 'parent' in your Category model
            return self.parent
        except Category.DoesNotExist:
            return None
    
    def get_all_categories_choices(self):
        """
        Get all categories and their descendants as choices.
        """
        categories = Category.objects.all()
        choices = [(category.slug, category.name) for category in categories.get_descendants(include_self=True)]
        return choices    
    def save(self, *args, **kwargs):
        # Check if the category is at level 0 and set the banner image accordingly
        if self.level == 0:
            self.banner_image = 'path_to_default_banner_image'  # Set the path to your default banner image
        else:
            self.banner_image = None

        super().save(*args, **kwargs)

class ServiceProviderType(models.Model):
    """
    ServiceProviderType Table will provide a list of the different types
    of ServiceProvider that are for sale.
    """

    name = models.CharField(verbose_name=_("service_provider_name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Service Provider Type")
        verbose_name_plural = _("Service Provider Types")

    def __str__(self):
        return self.name

class ServiceProviderSpecification(models.Model):
    """
    The ServiceProviderSpecification Table contains ServiceProvider
    specifiction or features for the Service Provider types.
    """

    service_provider_type = models.ForeignKey(ServiceProviderType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Service Provider Specification")
        verbose_name_plural = _("Service Provider Specifications")

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    """
    The Service Provider table contining all Service Providers items.
    """
    
    service_provider_type = models.ForeignKey(ServiceProviderType, on_delete=models.RESTRICT,null=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("title"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(unique=True,max_length=255)
    
    address = models.CharField(
        verbose_name=_("Address"),
        help_text=_("Business address"),
        max_length=255,
    )
    phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        help_text=_("Contact phone number"),
        max_length=20,
    )
    website = models.URLField(
        verbose_name=_("Website"),
        help_text=_("Business website URL"),
        blank=True,
        null=True,
    )
    
    rating = models.FloatField(
        verbose_name=_("Rating"),
        help_text=_("The average rating for the service provider"),
        blank=True,
        null=True,
        default=0,
    )
    
    is_active = models.BooleanField(
        verbose_name=_("service provider visibility"),
        help_text=_("Change service provider visibility"),
        default=True,
    )
    



    pinned_count = models.PositiveIntegerField(
            verbose_name=_("Pinned Count"),
            help_text=_("Number of users who pinned this service provider"),
            default=0,
        )


    owner = models.UUIDField(default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField('Tag', related_name='service_providers', blank=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Service_Providers")
        verbose_name_plural = _("Service_Providers")

    def get_absolute_url(self):
        return reverse("service_providers:Service Providers detail", args=[self.slug])

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name


class ServiceProviderSpecificationValue(models.Model):
    """
    The Service Provider Specification Value table holds each of the
    service provider's individual specification or bespoke features.
    """

    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='specification_values')
    specification = models.ForeignKey(ServiceProviderSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Value"),
        help_text=_("Service provider specification value (maximum of 255 characters)"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Service Provider Specification Value")
        verbose_name_plural = _("Service Provider Specification Values")

    def __str__(self):
        return self.value
class ServiceProviderImage(models.Model):
    """
    The Service Provider Image table.
    """

    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="service_provider_images")
    image = models.ImageField(
        verbose_name=_("Image"),
        help_text=_("Upload a service provider image"),
        upload_to="images/service_providers_images/",
        default="images/service_providers_images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alternative Text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Service Provider Image")
        verbose_name_plural = _("Service Provider Images")

class ServiceProviderReview(models.Model):
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, related_name="service_provider_reviews")
    user = models.UUIDField(default=uuid.uuid4, editable=False)
    rating = models.FloatField(default=0,)
    comment = models.TextField(max_length=1000, default="", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class SocialLink(models.Model):
    SOCIAL_TYPES = (
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
    )

    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='social_links', null=True, blank=True, default=None)
    social_type = models.CharField(
        verbose_name=_("Social Type"),
        help_text=_("Select the social media type"),
        choices=SOCIAL_TYPES,
        max_length=20,
        default='facebook',

    )
    url = models.URLField(
        verbose_name=_("Social Media URL"),
        help_text=_("Enter the URL for the social media profile"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Social Link")
        verbose_name_plural = _("Social Links")

    def __str__(self):
        return f"{self.get_social_type_display()} - {self.url}"

class ServiceProviderService(models.Model):
    """
    The Service Provider Service table containing the services of a service provider.
    """

    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(
        verbose_name=_("Service Name"),
        help_text=_("Required"),
        max_length=255,
    )
    
    price = models.DecimalField(
        verbose_name=_("Service Price"),
        help_text=_("Not Required"),
        max_digits=10,
        decimal_places=2,
    )
    
    description = models.TextField(
        verbose_name=_("Product Description"),
        help_text=_("Not Required"),
        blank=True,)
    
    icon = models.ImageField(
        upload_to='service_provider_icons/',
        verbose_name=_("Icon"),
        help_text=_("Upload an icon for the service provider service."),
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.service_provider.user.username}'s {self.name}"
