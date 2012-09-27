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
        'tx_lege_districts>=0.4.0',
    ],
    packages=find_packages('.', exclude=('exampleproject*',)),
    include_package_data=True,  # automatically include things from MANIFEST
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
