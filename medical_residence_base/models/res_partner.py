# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError

class Resident(models.Model):
    _inherit = "res.partner"

    residence_id = fields.Many2one(
        "rm.residence", 
        string=_("Residence"),
        track_visibility='onchange'
    )  # Resident residence
    employee_residence_id = fields.Many2one(
        "rm.residence", 
        string=_("Work Residence"),
        track_visibility='onchange'
    )  # Non resident residence (Employee contact)

    room_res_id = fields.Many2one(
        "rm.residence.room", 
        string=_("Room"),
        track_visibility='onchange'
    )  # Resident's room

    @api.onchange("residence_id")
    def reset_room(self):
        self.room_res_id = False

    def write(self, vals):
        if vals.get("room_res_id"):
            # Check new room capacity is not exceeded
            if self.room_res_id:
                if self.room_res_id[-1].id != vals.get(
                    "room_res_id"
                ):  # Check new room is different from previous room
                    new_room = self.env["rm.residence.room"].browse(
                        vals.get("room_res_id")
                    )
                    if new_room.capacity > len(new_room.resident_ids):
                        res = super(Resident, self).write(vals)
                        return res
                    else:
                        raise ValidationError(
                            _("New room capacity exceeded, room capacity: ")
                            + str(new_room.capacity)
                        )
            else:  # No previous room
                new_room = self.env["rm.residence.room"].browse(vals.get("room_res_id"))
                if new_room.capacity > len(new_room.resident_ids):
                    res = super(Resident, self).write(vals)
                    return res
                else:
                    raise ValidationError(
                        _("New room capacity exceeded, room capacity: ")
                        + str(new_room.capacity)
                    )
        return super(Resident, self).write(vals)

    def action_see_documents(self):
        # See partner documents
        directory_id = False
        folder = self.env["dms.directory"].sudo().search([])
        if self.employee_residence_id:
            for fold in folder:
                if (
                    fold.name == self.employee_residence_id.name
                    and fold.parent_id.name == _("Employees")
                ):  # From employee contact
                    directory_id = fold.id
        elif self.residence_id:
            for fold in folder:
                if fold.name == self.residence_id.name and fold.parent_id.name == _(
                    "Residents"
                ):  # From resident contact
                    directory_id = fold.id
        self.ensure_one()
        return {
            "name": _("Documents"),
            "res_model": "dms.file",
            "type": "ir.actions.act_window",
            "view_mode": "kanban,",
            "context": {
                "search_default_partner_id": self.id,
                "default_partner_id": self.id,
                "default_directory_id": directory_id,
                "searchpanel_default_directory_id": directory_id,
            },
        }
