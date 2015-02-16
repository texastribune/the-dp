from setuptools import setup

setup(
    name='tx_highered',
    version='0.3.4',
    description='Django app for Texas higher education data',
    author='Texas Tribune',
    author_email='tech@texastribune.org',
    url='http://github.com/texastribune/tx_highered/',
    license='Apache Software License',
    install_requires=[
        'tx_lege_districts>=0.4.0',
    ],
    packages=['tx_highered'],
    include_package_data=True,  # automatically include things from MANIFEST
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic'
    ],
)
