"""
Tests configuration for the cars app models.
"""

from django.test import TestCase
from .models import CarBrand, CarModel, CarYear


class CarModelTestCase(TestCase):
    """
    Test case for the CarBrand, CarModel, and CarYear models.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.brand = CarBrand.objects.create(name="TestBrand")
        self.model = CarModel.objects.create(brand=self.brand, name="TestModel")
        self.year = CarYear.objects.create(model=self.model, year=2023)

    def test_carbrand_str(self):
        """
        Test the __str__ method of CarBrand model.
        """
        self.assertEqual(str(self.brand), "TestBrand")

    def test_carmodel_str(self):
        """
        Test the __str__ method of CarModel model.
        """
        self.assertEqual(str(self.model), "TestBrand - TestModel")

    def test_caryear_str(self):
        """
        Test the __str__ method of CarYear model.
        """
        self.assertEqual(str(self.year), "TestBrand - TestModel - 2023")
