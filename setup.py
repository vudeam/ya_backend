from setuptools import setup

setup(
    name='Slasty App',
    version='0.1',
    packages=['slasty'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'sqlalchemy<=1.3.23',
        'flask-sqlalchemy',
        'python-dateutil'
    ]
)
