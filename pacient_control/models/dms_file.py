# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AnalysisDocument(models.Model):
    _inherit = "dms.file"
    task_id = fields.Many2one(
        "project.task", string=_("Analysis")
    )  # A document can belong to a task (Mainly for analysis task)
