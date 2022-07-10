from io import BytesIO

from PIL import Image
from autoslug import AutoSlugField
from django.core.files import File
from django.db import models

from product.utils import generate_key


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='slug_name')

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name', ]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    @property
    def slug_name(self):
        slug = f"{generate_key(6, 6)}-{self.name}"
        return slug


def make_thumbnail(image, size=(300, 200)):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)
    return thumbnail


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='slug_name')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
        indexes = [
            models.Index(fields=['name', 'description']),
        ]

    @property
    def slug_name(self):
        slug = f"{generate_key(6, 6)}-{self.name}"
        return slug

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
        return ''