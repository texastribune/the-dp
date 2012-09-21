from distutils.core import setup
import os.path

import tx_highered


def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )


def find_packages(path, base=""):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

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
    packages=find_packages('./tx_highered', 'tx_highered').keys(),
    package_data={
        'tx_highered': [
            'tx_highered/fixtures/*.json',
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
