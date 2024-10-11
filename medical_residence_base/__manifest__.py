# -*- coding: utf-8 -*-
{
    "name": "Residence Management",
    "summary": """
        Residence management project.""",
    "description": """
        Residence management
    """,
    "author": "Binhex",
    "website": "https://github.com/BinhexTeam/vertical-medical",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Medical",
    "version": "16.0.1.0",
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
        # Security
        "security/res_config_setting_security.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        # Data
        "data/hr_department_data.xml",
        "data/project_task_type_data.xml",
        "data/dms_tag_data.xml",
        # Views
        "views/residence_views.xml",
        "views/residence_type_views.xml",
        "views/rm_image_views.xml",
        "views/hr_expense_views.xml",
        "views/hr_employee_views.xml",
        "views/hr_applicant_views.xml",
        "views/res_partner_views.xml",
        "views/project_views.xml",
        "views/helpdesk_ticket_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "images": ["static/description/icon.png"],
    'assets': {
        'web.assets_backend': [
            "medical_residence_base/static/src/scss/image.scss"
        ]
    },
    "mantainer": ["szalatyzuzanna"],
}
