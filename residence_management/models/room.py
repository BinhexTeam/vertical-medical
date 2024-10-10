# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Room(models.Model):
    _name = "rm.residence.room"
    _description = "Residence Rooms"

    name = fields.Char(string=_("Name"), required=True)
    floor = fields.Integer(string=_("Floor"))

    resident_ids = fields.One2many("res.partner", "room_res_id", string=_("Resident"))

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))

    @api.depends("capacity", "resident_ids")
    def _compute_full(self):
        for record in self:
            if record.capacity > len(record.resident_ids):
                record.full = False
            else:
                record.full = True

    full = fields.Boolean(compute=_compute_full, string=_("Full"), store=True)

    sq_meters = fields.Integer(string=_("Square Meters"))
    bathroom = fields.Boolean(string=_("Internal Bathroom"))
    capacity = fields.Integer(string=_("Capacity"), default=1)

    @api.onchange("capacity")
    def check_capacity(self):
        if self.capacity < len(self.resident_ids):
            raise ValidationError(
                _("Capacity cant be less than number of residents in the room.")
            )

    @api.onchange("resident_ids")
    def check_residents(self):
        if len(self.resident_ids) > self.capacity:
            raise ValidationError(_("Room capacity exceeded"))
