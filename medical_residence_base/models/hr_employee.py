# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _

class Employee(models.Model):
    _inherit = "hr.employee"

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
    residence_ids = fields.Many2many(comodel_name="rm.residence",
        relation="residence_employee_table_1",
        column1="res_id",
        column2="emp_id",
        string=_("Residences"))
   

class EmployeePublic(models.Model):
    _inherit = "hr.employee.public"
    residence_id = fields.Many2one("rm.residence")
