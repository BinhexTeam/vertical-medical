from odoo import models, fields, api, _


class Journal(models.Model):
    _inherit = "account.journal"

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
