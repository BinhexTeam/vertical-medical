# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
import datetime


class Residence(models.Model):
    _name = "residence.residence"
    _description = "Residence"
    _inherit = ["mail.thread", "mail.activity.mixin"] 

    # Fields
    name = fields.Char(string=_("Name"), required=True)
    description = fields.Text(string=_("Description"))
    image = fields.Binary(string=_("Image"))
    manager_id = fields.Many2one("hr.employee", string=_("Manager"))
    phone = fields.Char(string=_("Phone"),unaccent=False)
    email = fields.Char(string=_("Email"))

    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")

    # Relations
    type_id = fields.Many2one("residence.type", string=_("Type"))
    room_ids = fields.One2many("residence.room", "residence_id", string=_("Rooms"))
    employee_ids = fields.Many2many("hr.employee", string=_("Employees"))
    project_id = fields.Many2one("project.project", string=_("Project"))
    #resident_ids = fields.One2many("res.partner", "residence_id", string=_("Resident"))
    #employee_resident_ids = fields.One2many(
    #    "res.partner", "employee_residence_id", string=_("Resident")
    #)

    #expense_ids = fields.One2many("hr.expense", "residence_id", string=_("Expenses"))

   
    '''public_employees = fields.One2many(
        "hr.employee.public", "residence_id", string=_("Employees")
    )

    employee_contact_ids = fields.One2many(
        "res.partner", "employee_residence_id", string=_("Employees")
    )'''
    #recruitment_ids = fields.One2many(
    #    "hr.applicant", "residence_id", string=_("Recruitments")
    #)

    #project_ids = fields.One2many(
    #    "project.project", "residence_id", string=_("Projects")
    #)

    #ticket_ids = fields.One2many("helpdesk.ticket", "residence_id", string=_("Tickets"))
    #directory_ids = fields.One2many("dms.directory", "residence_id")

    @api.constrains("email")
    def _check_email(self):
        for residence in self:
            if residence.email:
                match = re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,5})$",residence.email)
                if not match:
                    raise ValidationError(_("Not a valid E-mail"))


class ResidenceType(models.Model):
    _name = "residence.type"
    _description = "Residence Type"

    name = fields.Char(string=_("Name"), required=True)
    residence_ids = fields.One2many("residence.residence", "type_id", string="Residences")

class ResidenceFloor(models.Model):
    _name = "residence.floor"
    _description = "Residence Floors"

    name = fields.Char(string=_("Name"), required=True)
    room_ids = fields.One2many("residence.room", "floor_id", string=_("Rooms"))
    residence_id = fields.Many2one("residence.residence", string=_("Residence"))


class ResidenceRoom(models.Model):
    _name = "residence.room"
    _description = "Residence Rooms"
    _order = "floor_id, name"

    name = fields.Char(string=_("Name"), required=True)
    floor_id = fields.Many2one("residence.floor", string=_("Floor"))
    resident_ids = fields.One2many("res.partner", "room_id", string=_("Residents"))
    residence_id = fields.Many2one(related="floor_id.residence_id", string=_("Residence"))

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

    residence_id = fields.Many2one("residence.residence", string=_("Residence"))

    def action_show_residents(self):
        return {
            'name': "Residents",
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban',
            'res_model': 'res.partner',
            'view_id': self.env.ref('base.res_partner_kanban_view').id,
            'target': 'current',
            'domain': [('room_id', '=', self.id)]
        }