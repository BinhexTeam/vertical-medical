# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _, SUPERUSER_ID
import re
from odoo.exceptions import ValidationError

class HelpdesktTeam(models.Model):
    _inherit = "helpdesk.ticket.team"
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
