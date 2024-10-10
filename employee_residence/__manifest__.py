# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
{
    "name": "Residence Employee",
    "summary": """
        Residence Employee""",
    "author": "Binhex",
    "website": "https://github.com/BinhexTeam/vertical-medical",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Medical",
    "version": "16.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["residence_management", "hr_recruitment"],
    # always loaded
    "data": [
        "views/hr_employee_views.xml",
        "views/hr_jobs_views.xml",
    ],
    "mantainer": ["szalatyzuzanna"],
}
