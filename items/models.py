from django.db import models


class Category(models.Model):

    class Meta: 
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=150)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Item(models.Model):
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    vintage = models.TextField(null=True, default="")
    size = models.TextField(null=True, default="")
    colour = models.TextField(null=True, default="")
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=100, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
