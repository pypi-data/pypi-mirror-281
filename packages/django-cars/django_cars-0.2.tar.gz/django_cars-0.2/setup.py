from setuptools import setup, find_packages

setup(
    name='django_cars',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app for managing car data',
    long_description=open('docs/README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jafar-sadigzade/django_cars',
    author='Jafar Sadigzade',
    author_email='jafarsadigzade@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=5.0',
    ],
)
