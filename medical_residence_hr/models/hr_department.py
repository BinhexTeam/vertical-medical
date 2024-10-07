# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _

class Department(models.Model):
    _inherit = "hr.department"
    # Adding expenses to the department
    expense_ids = fields.One2many(
        "hr.expense", "department_id", string=_("Expenses")
    )  # Adds relation to expense