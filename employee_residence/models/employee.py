from odoo import models, fields, api, _


class Employee(models.Model):
    _inherit = "hr.employee"

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))


# class Residence(models.Model):
#     _inherit = "rm.residence"

#     employee_ids = fields.One2many("hr.employee", "residence_id", string=_("Employees"))
