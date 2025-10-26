# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'EOD Rental Order',
    'version': '1.0',
    'depends': ['base','mail','account'],
    'author': 'EasyOutDesk',
    'maintainer':'Easy Outdesk',
    'category': 'Custom module',
    'summary': 'Custom module for EasyOutDesk Rental',
    'description': 'This module was created for Handling the Bike rental Process.',
    'data': [
        'security/ir.model.access.csv',
        'security/security_group.xml',
        'data/rental_order_sequence.xml',
        'views/eod_rental_order_view.xml',
        'views/eod_bike_views.xml',
        'views/bike_brand_views.xml',
        'views/bike_shop_view.xml',
        'wizard/bike_request_reject_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}