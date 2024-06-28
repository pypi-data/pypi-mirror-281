# Django Cars

A Django application for managing car data. This package provides functionality for loading and managing car data within a Django project.

## Features

- Load car data from a custom management command
- Manage car data within a Django admin interface
- Easy integration into existing Django projects

## Installation

You can install the package via pip:

```shell
pip install django_cars
```
## Usage
 - Add cars to your INSTALLED_APPS in your Django settings file:
```shell
# settings.py
INSTALLED_APPS = [
    ...,
    'cars',
]
```
 - Run the migrations to set up the database tables:
```shell
python manage.py migrate

```
 - Load the car data using the custom management command:
```shell
python manage.py load_car_data
```

# Development
## Setting Up a Development Environment

 - Clone the repository:
```shell
git clone https://github.com/yourusername/django_cars.git
cd django_cars
```
 - Create a virtual environment and activate it:
```shell
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
 - Install the development dependencies:
```shell
pip install -r requirements.txt
```
 - Run the Django development server:
```shell
python manage.py runserver
```
## Running Tests
To run the tests for this project, use the following command:
```shell
python manage.py test
```
# Contributing
## Contributions are welcome! Please open an issue or submit a pull request for any changes.

# License
### This project is licensed under the MIT License. See the LICENSE file for more details.

# Acknowledgements
This project was inspired by the need for an efficient way to manage car data within Django applications.
Special thanks to the Django community for their continuous support and contributions.

# Contact
### For any questions or feedback, feel free to reach out:

 - Email: jafarsadigzade@gmail.com
 - Phone: +994709924546