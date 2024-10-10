# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _


class Image(models.Model):
    _name = "rm.image"
    _order = "name"
    _description = "Images"

    # Fields

    name = fields.Char(string=_("Name"))
    image = fields.Binary(string=_("Image"), required=True)

    # Relations

    residence_id = fields.Many2one("rm.residence", string="Residence")
