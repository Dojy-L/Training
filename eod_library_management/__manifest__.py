# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Library Management',
    'version': '19.0.0.0.0',
    'depends': ['base','mail','contacts','website','portal','web_map'],
    'author': 'EasyOutDesk',
    'maintainer': 'Dojy Larsan',
    'website': 'https://www.easyoutdesk.com',
    'category': 'Custom',
    'summary': 'Custom module for Library management',
    'description': 'This module helps manage library operations',
    'data': [
        'data/sequence.xml',
        'data/ir_module_category_data.xml',
        'data/website_menu_book.xml',

        'security/ir.model.access.csv',
        'security/security_group.xml',
        'security/security_rule.xml',
        'views/library_menus.xml',
        'views/library_book_view.xml',
        'views/book_rental_view.xml',
        'views/res_partner_view.xml',
        'views/overdue_rentals.xml',
        'views/ongoing_rental_view.xml',
        'views/books_template.xml',
        'views/portal_view_rental_template.xml',
        'views/fine_template.xml',
        'views/overdue_template.xml',

        'report/ongoing_report_action.xml',
        'report/ongoing_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
