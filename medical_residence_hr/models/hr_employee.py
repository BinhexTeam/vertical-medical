# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _

class Employee(models.Model):
    _inherit = "hr.employee"
    
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))

