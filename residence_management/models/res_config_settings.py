# -*- coding: utf-8 -*-

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]

    # Residence settings

    group_employee = fields.Boolean(
        string=_("Employees Contact"),
        implied_group="residence_management.group_employee",
    )
