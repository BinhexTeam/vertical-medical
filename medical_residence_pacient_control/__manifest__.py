# -*- coding: utf-8 -*-
{
    "name": "Pacient Control",
    "summary": """
        Pacient control.""",
    "author": "Binhex",
    "website": "https://github.com/BinhexTeam/vertical-medical",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Medical",
    "version": "16.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["medical_residence_pacient", "calendar", "medical_residence_base","product"],
    # always loaded
    "data": [
        # Data
        "data/task_types.xml",
        "data/mail_template.xml",
        "data/hygiene_elems.xml",
        "data/appointment_types.xml",
        "data/product_category.xml",
        # Security
        "security/ir.model.access.csv",
        "security/res_config_settings_security.xml",
        # Wizards
        "wizards/rm_resident_treatment_wizard_views.xml",
        # Views
        "views/project_task_views.xml",
        "views/res_partner_views.xml",
        "views/res_config_settings_views.xml",
        "views/rm_resident_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "mantainer": ["szalatyzuzanna"],
}
