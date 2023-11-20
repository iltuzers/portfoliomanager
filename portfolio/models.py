from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class Stock(models.Model):
    symbol = models.CharField(max_length=32, unique=True)
    class Meta:
        ordering = ['symbol']
    
    def __str__(self):
        return self.symbol
    
    def get_absolute_url(self):
        return reverse('stock-detail', args=[str(self.id)])




class Option(models.Model):
    symbol = models.CharField(max_length=32, unique=True)
    underlying = models.ForeignKey(Stock, on_delete=models.CASCADE)
    expiration_date = models.DateField()
    strike = models.DecimalField(max_digits=10, decimal_places=2)
    OPTION_TYPE = (
        ('C', 'Call'),
        ('P', 'Put'),
    )
    option_type = models.CharField(
        max_length = 1,
        choices = OPTION_TYPE,
        help_text = 'Option Type: Put or Call'
    )
    
    class Meta:
        ordering = ['expiration_date', 'symbol', 'strike']
        unique_together = [['underlying', 'expiration_date', 'strike', 'option_type']]
    
    def __str__(self):
        return self.symbol
    
    def get_absolute_url(self):
        return reverse('option-detail', args=[str(self.id)])



class Portfolio(models.Model):
    INSTRUMENT_TYPE = (
        ('O', 'Option'),
        ('S', 'Stock'),
    )
    instrument_type = models.CharField(
        max_length = 1,
        choices = INSTRUMENT_TYPE,
        help_text = 'Stock or Option Type',
    )
    name = models.CharField(max_length=32, default="Default") # may change this to username
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ManyToManyField(Stock, blank=True, null=True) # Either stock or option should not be null
    option = models.ManyToManyField(Option, blank=True, null=True)

    # negative if short, positive if long
    quantity = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['owner']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[str(self.id)])
    
    
    