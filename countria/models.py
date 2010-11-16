from django.db import models
from lingua import translation
from decimal import Decimal
import settings

class Currency(models.Model):
    class Translation(translation.Translation):
        name   = models.CharField(max_length=16)
    code   = models.CharField(max_length=3) 

    class Meta:
        unique_together = (('name','code'), )

    def __unicode__(self):
        return unicode(self.name)

class Continent(models.Model):
    class Translation(translation.Translation):
        name   = models.CharField(max_length=16)
    code   = models.CharField(max_length=2) 

    class Meta:
        unique_together = (('name','code'), )

    def __unicode__(self):
        return unicode(self.name)

class Country(models.Model):
    class Translation(translation.Translation):
        name      = models.CharField(max_length=64, unique=True)
        full_name = models.CharField(max_length=64)

    currency        = models.ForeignKey(Currency, null=True)
    sovereignty     = models.ForeignKey('self', null=True)
    capital         = models.ForeignKey('City', null=True, related_name="country_capital")   
    idc             = models.PositiveIntegerField(null=True) # Iternational Dialing Code
    iso_2           = models.CharField(max_length=2, null=True)
    iso_3           = models.CharField(max_length=3, null=True)
    iso_number      = models.PositiveIntegerField(null=True)
    tld             = models.CharField(max_length=7, null=True)
    latitude        = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal("0.0"))
    longitude       = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal("0.0"))
    population      = models.PositiveIntegerField(null=True)
    continent       = models.ForeignKey(Continent, null=True)

    def __calling_code(self):
        return '00%d' % self.idc
    
    calling_code = property(__calling_code)

    def __unicode__(self):
        if hasattr(settings, 'MAX_COUNTRY_NAME_LENGTH'):
            if len(self.name) > settings.MAX_COUNTRY_NAME_LENGTH:
                return self.name[:settings.MAX_COUNTRY_NAME_LENGTH] + '...'
        return unicode(self.name)

class City(models.Model):
    class Translation(translation.Translation):
        name = models.CharField(max_length=64)

    country     = models.ForeignKey(Country, null=True)
    state       = models.ForeignKey('State', null=True)
    population  = models.PositiveIntegerField(null=True)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal("0.0"))
    longitude   = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal("0.0"))

    def __unicode__(self):
        return unicode(self.name)

class State(models.Model):
    class Translation(translation.Translation):
        name = models.CharField(max_length=64)

    capital     = models.ForeignKey('City', related_name="state_capital", null=True)
    country     = models.ForeignKey(Country, related_name="state_country", null=True)
    latitude    = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal("0.0"))
    longitude   = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal("0.0"))
    code        = models.CharField(max_length=2)

    def __unicode__(self):
        return unicode(self.name)

