from setuptools import find_packages
from distutils.core import setup

setup(
    name='tx_highered',
    version='0.2alpha.0',
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
