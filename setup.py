import setuptools

setuptools.setup(
    name='flight_raccoon',
    version='1.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'flight_raccoon = flight_raccoon.command_line:main'
        ]
    },
    author='Vlaidmir Demidov',
    description='This is a flight raccoon, it will help you to find the best flight for your next vacation',
    python_requires=' >= 3.7'
)