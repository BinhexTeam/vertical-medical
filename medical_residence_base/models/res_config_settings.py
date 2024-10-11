# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings"]
    # Residence settings
    group_employee = fields.Boolean(
        string=_("Employees Contact"),
        implied_group="medical_residence_base.group_employee",
    )
