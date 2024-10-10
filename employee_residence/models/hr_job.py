# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _

class HrJob(models.Model):
    _inherit = "hr.job"
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
