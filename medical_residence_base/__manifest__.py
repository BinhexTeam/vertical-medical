# -*- coding: utf-8 -*-
{
    'name': "Residence Base",

    'summary': """
        Residence management base.""",

    'description': """
        Residence management base.
    """,

    'author': "Binhex",
    'website': "https://github.com/BinhexTeam/vertical-medical",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Medical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project',"hr_expense"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/residence_security.xml',
        'views/residence_views.xml',
    ],
}
