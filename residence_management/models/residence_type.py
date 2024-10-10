# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Type(models.Model):
    _name = "rm.residence.type"
    _description = "Residence Type"

    name = fields.Char(string=_("Name"), required=True)

    residence_ids = fields.One2many("rm.residence", "type_id", string="Residences")
