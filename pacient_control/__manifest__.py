# -*- coding: utf-8 -*-
{
    "name": "Pacient Control",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "pacient_management", "calendar", "residence_management"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/task_types.xml",
        "wizards/create_treatment.xml",
        "views/project_task.xml",
        "views/res_partner.xml",
        "data/mail_template.xml",
        "data/hygiene_elems.xml",
        "data/appointment_types.xml",
        "views/res_config_settings.xml",
        "data/product_category.xml",
        "security/res_config_settings_security.xml",
        "views/treatment.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # "demo/demo.xml",
    ],
    "images": ["static/description/icon.png"],
}
