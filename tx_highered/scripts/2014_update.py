#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Automate migrating the data from launch state to what we need in 2014.

You only need to run this once, but it's safe to run repeatedly.
"""
from __future__ import unicode_literals

from tx_highered.models import Institution


def associate_districts():
    """
    Associate existing districts with ids so we can import to them.
    """
    institution = Institution.objects.get(slug='alamo-community-college-district')
    institution.fice_id = '003607'
    institution.ipeds_id = '222497'
    institution.save()

    institution = Institution.objects.get(slug='dallas-county-community-college-district')
    institution.fice_id = '009331'
    institution.ipeds_id = '224253'
    institution.save()

    institution = Institution.objects.get(slug='howard-county-junior-college-district')
    institution.fice_id = '103574'
    institution.save()

    institution = Institution.objects.get(slug='lone-star-college-system-district')
    institution.fice_id = '011145'
    # lone star already has an ipeds id
    institution.save()

    institution = Institution.objects.get(slug='san-jacinto-community-college')
    institution.fice_id = '029137'
    # San Jacinto College Central Campus has the ipeds id for the system
    institution.save()

    institution = Institution.objects.get(slug='tarrant-county-college-district')
    institution.fice_id = '003626'
    institution.ipeds_id = '228547'
    institution.save()


def add_new_institutions():
    Institution.objects.get_or_create(
        slug='lone-star-college-university-park',
        fice_id='000821',
        defaults=dict(
            name='Lone Star College - University Park',
            address='20515 SH 249',
            city='Houston',
            zip_code='77070-2607',
            phone='281-290-2600',
            url='http://www.lonestar.edu/universitypark.htm',
            location='POINT(-95.57932 29.99093)',
            institution_type='pub_cc',
            system_id=11,
        ),
    )


def fix_old_institutions():
    # This is a private law school, which is beyond the scope of this explorer
    institution = Institution.objects.get(slug='south-texas-college-of-law')
    institution.ipeds_id = None
    institution.save()


if __name__ == '__main__':
    add_new_institutions()
    associate_districts()
    fix_old_institutions()
