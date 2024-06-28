"""
Models configuration for the 'cars' app.
"""

from django.db import models


class CarBrand(models.Model):
    """
    Model for car brands.
    """
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        Returns a string representation of the CarBrand instance.

        Returns:
            str: A string representing the name of the car.
        """
        return self.name


class CarModel(models.Model):
    """
    Model for car models.
    """
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        Returns a string representation of the CarModel instance.

        Returns:
            str: A string representing the brand and name of the car.
        """
        return f"{self.brand} - {self.name}"


class CarYear(models.Model):
    """
    Model for car years.
    """
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    def __str__(self) -> str:
        """
        Returns a string representation of the CarYear instance.

        Returns:
            str: A string representing the model and year of the car.
        """
        return f"{self.model} - {self.year}"


class CarSpecification(models.Model):
    """
    Model for car specifications (horsepower and engine cc).
    """
    car_year = models.ForeignKey(CarYear, on_delete=models.CASCADE)
    horsepower = models.PositiveIntegerField()
    engine_cc = models.PositiveIntegerField()

    def __str__(self) -> str:
        """
        Returns a string representation of the CarSpecification instance.

        Returns:
            str: A string representing the car year, horsepower, and engine cc.
        """
        return f"{self.car_year} - {self.horsepower} HP - {self.engine_cc} cc"
