
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Sum

# Create your models here.
class SKU(models.Model):
    slug = models.SlugField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True, blank = True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return str(self.slug) + " | " + str(self.name[:25])

    def get_absolute_url(self):
        return reverse('sku-detail', kwargs={'slug': self.slug})

    def avg_cost(self):
        #exclude yg otw, exclude yg kejual
        avg = Product.objects.filter(sku=self).exclude(location__slug='in').exclude(location__slug='out').aggregate(Avg('cost'))['cost__avg']
        if avg:
            return round(avg)
        else:
            return "-"

    def avg_price(self):
        #hanya yg kejual
        avg = Product.objects.filter(sku=self).aggregate(Avg('price'))['price__avg']
        if avg:
            return round(avg)
        else:
            return "-"


class Warehouse(models.Model):
    slug = models.SlugField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return "WH : " + self.slug

    def get_absolute_url(self):
        return reverse('warehouse-detail', kwargs={'slug': self.slug})

class Marketplace(models.Model):
    slug = models.SlugField(max_length=50, null=True, unique=True)
    name = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('marketplace-detail', kwargs={'slug': self.slug})

class Inbound(models.Model):
    code = models.CharField(max_length=255, null=True, unique=True)
    total_paid_cost = models.FloatField(null=True)
    note = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.code

    def total_cost(self):
        sum = Product.objects.filter(inbound_order=self).aggregate(Sum('cost'))['cost__sum']
        if sum:
            return round(sum)
        else:
            return "-"

    def discount(self):
        if isinstance(self.total_cost(), str):
            return "-"
        else:
            disc = 1 - self.total_paid_cost/self.total_cost()
            if disc:
                return [disc, f'{round(disc*100,1)}%']
            else:
                return [disc, '']


class Outbound(models.Model):
    code = models.CharField(max_length=255, null=True, unique=True)
    total_sold_price = models.FloatField(null=True)
    note = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    marketplace = models.ForeignKey(Marketplace, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.code


class Product(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, null=True, related_name='productsku_set')
    exp_date = models.DateTimeField(null=True, blank=True)
    cost = models.FloatField(null=True)
    price = models.FloatField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    inbound_order = models.ForeignKey(Inbound, on_delete=models.SET_NULL, null=True)
    outbound_order = models.ForeignKey(Outbound, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.sku.slug +" ("+str(self.id)+")"

    def cost_view(self):
        return round(self.cost ,2)


class TestProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name) + str(self.price)