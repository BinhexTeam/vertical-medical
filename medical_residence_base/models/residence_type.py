# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _

class Type(models.Model):
    _name = "rm.residence.type"
    _description = "Residence Type"
    
    
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        ondelete='restrict',
        default=lambda self: self.env.company.id
    )
       
    name = fields.Char(string=_("Name"), required=True)
    residence_ids = fields.One2many("rm.residence", "type_id", string="Residences")
