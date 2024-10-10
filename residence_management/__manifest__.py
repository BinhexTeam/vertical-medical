# -*- coding: utf-8 -*-
{
    "name": "Residence Management",
    "summary": """
        Residence management project.""",
    "description": """
        Residence management
    """,
    "author": "Binhex Systems Solutions S.L.",
    "website": "https://binhex.es/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "hr_expense",
        "dms",
        "l10n_es",
        "hr",
        "hr_recruitment",
        "project",
        "helpdesk_mgmt",
        "helpdesk_type",
    ],
    # always loaded
    "data": [
        "data/departments.xml",
        "security/res_config_setting_security.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/residence.xml",
        "views/residence_type.xml",
        "views/image.xml",
        "views/expense.xml",
        "views/room.xml",
        "views/employee.xml",
        "views/recruitment.xml",
        "views/res_partner.xml",
        "views/journal.xml",
        "data/tags.xml",
        "data/stages.xml",
        "views/project.xml",
        "views/helpdesk.xml",
        "views/res_config_settings_views.xml",
    ],
    "images": ["static/description/icon.png"],
    'assets': {
        'web.assets_backend': [
            "residence_management/static/src/scss/image.scss"
        ]
    },
    # 'post_init_hook': 'post_init_hook',
}
