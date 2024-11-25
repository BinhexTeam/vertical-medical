# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
{
    "name": "Pacient Management",
    "summary": """
        Pacient management.""",
    "author": "Binhex",
    "website": "https://github.com/BinhexTeam/vertical-medical",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Medical",
    "version": "16.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["dms", "medical_residence_base"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/dms_file_views.xml",
        "views/res_partner_resident_views.xml",
        "views/res_partner_family_views.xml",
        "views/rm_resident_relationship_type_views.xml",
        "views/rm_resident_relationship_legal_views.xml"
    ],
    "images": ["static/description/icon.png"],
    'assets': {
        'web.assets_backend': [
            "medical_residence_base/static/src/scss/image.scss"
        ]
    },
    "mantainer": ["szalatyzuzanna"],
}
