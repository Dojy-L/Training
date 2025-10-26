# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'version': '19.0.0.0.0',
    'depends': ['base'],
    'author': 'EasyOutDesk',
    'maintainer':'Easy Outdesk',
    'category': 'Custom module',
    'summary': 'Custom module for EasyOutDesk Rental',
    'description': 'This module was created for Handling the Bike rental Process.',
    'data': [
        'security/res_group.xml',
        'security/ir.model.access.csv',
        'views/estate_menu.xml',
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}