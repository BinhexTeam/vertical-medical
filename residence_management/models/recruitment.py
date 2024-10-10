from odoo import models, fields, api, _


class recruitment_job(models.Model):
    _inherit = "hr.applicant"

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
