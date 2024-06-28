"""
Management command to load car brands, models, and years into the database.
"""

from django.core.management.base import BaseCommand
from cars.models import CarBrand, CarModel, CarYear, CarSpecification
from cars.car_data import car_data
from tqdm import tqdm


class Command(BaseCommand):
    """
    Command class to load car data.
    """
    help = 'Load car brands, models, and years into the database'

    def handle(self, *args, **kwargs):
        """
        Load car data into the database.
        """
        total_brands = len(car_data)
        total_models = sum(len(models) for models in car_data.values())
        total_years = sum(len(years['years']) for models in car_data.values() for years in models.values())
        total_specs = sum(len(specs) for models in car_data.values() for years in models.values() for specs in years['years'].values())

        with tqdm(total=total_brands + total_models + total_years + total_specs, desc="Loading car data", unit="entry") as pbar:
            for brand_name, models in car_data.items():
                brand, created = CarBrand.objects.get_or_create(name=brand_name)
                pbar.update(1)
                for model_name, model_data in models.items():
                    model, created = CarModel.objects.get_or_create(brand=brand, name=model_name)
                    pbar.update(1)
                    for year, specs in model_data['years'].items():
                        car_year, created = CarYear.objects.get_or_create(model=model, year=year)
                        pbar.update(1)
                        for spec in specs:
                            CarSpecification.objects.get_or_create(
                                car_year=car_year,
                                horsepower=spec['horsepower'],
                                engine_cc=spec['engine_cc']
                            )
                            pbar.update(1)

        self.stdout.write(self.style.SUCCESS('Successfully loaded car data'))
