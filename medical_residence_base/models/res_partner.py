# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError

class Resident(models.Model):
    _inherit = "res.partner"

    residence_id = fields.Many2one(
        "rm.residence", 
        string=_("Residence"),  
    )  # Resident residence
    
    employee_residence_id = fields.Many2one(
        "rm.residence", 
        string=_("Work Residence"),
        
    )  # Non resident residence (Employee contact)
    

    room_res_id = fields.Many2one(
        "rm.residence.room", 
        string=_("Room"),
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
    
  