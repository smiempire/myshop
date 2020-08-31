import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from stdimage import StdImageField


# ========================================= Abstract models ========================================= #

class BaseModel(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

# ========================================= /Abstract models ========================================= #


# ============================================ User data ============================================= #

class UserProfile(models.Model):
    ip = models.CharField(max_length=40, blank=True)
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.django_user.email

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'


class Visitor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', related_name='product_visitor', on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'
        ordering = ['-created']


# ============================================ /User data ============================================= #


# =========================================== Product data ============================================ #

class Category(BaseModel):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class ProductImage(models.Model):
    image = StdImageField("Image", upload_to='product/image/%Y/%m/%d', variations={
        'thumbnail': (153, 153, True), 'medium': (263, 263, True), 'large': (600, 600, True)})

    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.filter(is_available=True)


class Product(BaseModel):
    category = models.ManyToManyField(Category, related_name='category_product')
    image = models.ManyToManyField(ProductImage, blank=True, related_name='image_product')
    price = models.DecimalField(u"Price", decimal_places=2, max_digits=10, default=0)
    is_available = models.BooleanField(default=True)
    views = models.IntegerField(u'Views', default=0)
    objects = ProductQuerySet.as_manager()

    def is_new(self):
        date_limit = timezone.now() - datetime.timedelta(days=30)
        if self.created > date_limit:
            return True
        return False

    def get_price(self):
        return '{0:,}'.format(self.price).replace(',', ' ')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ["name"]

# =========================================== /Product data ============================================ #
