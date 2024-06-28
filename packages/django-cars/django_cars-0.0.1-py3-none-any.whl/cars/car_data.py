"""
Data for car brands, models, and their production years.
"""

car_data = {
    'Acura': {
        'ILX': {
            'years': {
                2012: [{'horsepower': 201, 'engine_cc': 2000}],
                2013: [
                    {'horsepower': 201, 'engine_cc': 2000},
                    {'horsepower': 201, 'engine_cc': 1800},
                    {'horsepower': 240, 'engine_cc': 2000}
                ],
                2016: [{'horsepower': 240, 'engine_cc': 2800}],
            }
        },
        'MDX': {
            'years': {
                2000: [{'horsepower': 240, 'engine_cc': 3200}],
                2023: [{'horsepower': 290, 'engine_cc': 3500}],
            }
        },
        'ZDX': {
            'years': {
                2010: [{'horsepower': 300, 'engine_cc': 3600}],
                2013: [{'horsepower': 300, 'engine_cc': 3600}],
            }
        },
    },
    'Alfa Romeo': {
        '147': {
            'years': {
                2000: [{'horsepower': 120, 'engine_cc': 1600}],
                2010: [{'horsepower': 150, 'engine_cc': 1800}],
            }
        },
        '159': {
            'years': {
                2005: [{'horsepower': 200, 'engine_cc': 2000}],
                2011: [{'horsepower': 210, 'engine_cc': 2200}],
            }
        },
        'Giulia': {
            'years': {
                1962: [{'horsepower': 110, 'engine_cc': 1600}],
                1978: [{'horsepower': 130, 'engine_cc': 1800}],
            }
        },
        'Stelvio': {
            'years': {
                2016: [{'horsepower': 280, 'engine_cc': 2000}],
                2023: [{'horsepower': 280, 'engine_cc': 2000}],
            }
        },
    },
}
