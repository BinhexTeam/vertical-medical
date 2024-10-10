from odoo import models, fields, api, _, SUPERUSER_ID
import re
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class HelpdesktTypeTicket(models.Model):
    _inherit = "helpdesk.ticket.type"

    helpdesk_team_ids = fields.Many2many(
        "helpdesk.ticket.team", "helpdesk_ticket_type_id", string=_("Teams")
    )


class HelpdesktTeam(models.Model):
    _inherit = "helpdesk.ticket.team"

    helpdesk_ticket_type_id = fields.Many2one(
        "helpdesk.ticket.type", string=_("Ticket Type")
    )


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    # Assign tickets to a residence
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))

    @api.onchange("partner_id")
    def update_residence_id(self):
        if self.partner_id.residence_id:
            self.residence_id = self.partner_id.residence_id
        else:
            self.residence_id = False
