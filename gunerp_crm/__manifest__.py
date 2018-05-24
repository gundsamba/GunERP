# -*- coding: utf-8 -*-
{
    'name': "Хэрэглэгчийн харилцааны менежмент",

    'summary': """
        Хэрэглэгчийн харилцааны менежментийн систем
    """,

    'description': """
        Хэрэглэгчийн харилцааны менежментийн систем
    """,

    'author': "EGO:Tech LLC - Gundsamba Gantumur",
    'website': "http://www.egotech.mn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','point_of_sale'],

    # always loaded
    'data': [
        'views/mn_state.xml',
        'views/templates.xml',
        'views/roles.xml',
        'views/user.xml',
        'views/company.xml',
        'views/customer.xml',
        'views/pos_dashboard.xml',
        'views/view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
        "static/src/xml/templates.xml",
    ],
    'application': True,
}
