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

    @api.onchange("partner_id")
    def update_residence_id(self):
        if self.partner_id.residence_id:
            self.residence_id = self.partner_id.residence_id
        elif self.team_id and self.team_id.residence_id:
            self.residence_id = self.team_id.residence_id.id
        else:
            self.residence_id = False
