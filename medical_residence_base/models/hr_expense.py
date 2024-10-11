# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, tools, _

class Spendings(models.Model):
    _inherit = "hr.expense"
    # Assign expense to a department and a residence
    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
    department_id = fields.Many2one("hr.department", string=_("Department"))

    @api.onchange("employee_id")
    def get_department_employee(self):
        self.department_id = self.employee_id.department_id

    @api.onchange("residence_id")
    def clean_department_employee(self):
        self.employee_id = False
        self.department_id = False
