"""
Admin configuration for the 'cars' app.
"""

from django.contrib import admin
from .models import CarBrand, CarModel, CarYear, CarSpecification

# Register your models here.
admin.site.register(CarBrand)
admin.site.register(CarModel)
admin.site.register(CarYear)
admin.site.register(CarSpecification)
