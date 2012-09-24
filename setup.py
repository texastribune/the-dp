from setuptools import find_packages
from distutils.core import setup

import tx_highered

setup(
    name='tx_highered',
    version=tx_highered.__version__,
    description='Django app for Texas higher education data',
    author='Texas Tribune',
    author_email='tech@texastribune.org',
    url='http://github.com/texastribune/tx_highered/',
    license='Apache Software License',
    install_requires=[
        'geopy',
    ],
    packages=find_packages('.', exclude=('exampleproject*',)),
    package_data={
        'tx_highered': [
            'tx_highered/fixtures/*.json',
            'templates/*.html',
            'templates/*/*.html',
            'templates/*/*/*.html',
            'static/*.css',
            'static/*/*.css',
            'static/*/*/*.css',
            'static/*.js',
            'static/*/*.js',
            'static/*/*/*.js',
            'static/*.png',
            'static/*/*.png',
            'static/*/*/*.png',
            'static/*.jpg',
            'static/*/*.jpg',
            'static/*/*/*.jpg',
            'static/*.jpeg',
            'static/*/*.jpeg',
            'static/*/*/*.jpeg',
            'static/*.gif',
            'static/*/*.gif',
            'static/*/*/*.gif',
            '*.exe',  # WHATEVER I DON'T CARE I HATE PYTHON
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/NonlistedTopic'
    ],
)
