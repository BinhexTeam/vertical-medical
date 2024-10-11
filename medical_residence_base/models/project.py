# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError

class Project(models.Model):
    _inherit = "project.project"
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
