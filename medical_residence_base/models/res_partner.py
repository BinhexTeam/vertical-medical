# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, tools, _
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class Resident(models.Model):
    _inherit = "res.partner"

    room_id = fields.Many2one(
        "residence.room", 
        string=_("Room"),
        track_visibility='onchange'
    ) 
    residence_id = fields.Many2one(
        related="room_id.residence_id",
        string=_("Residence")
    )