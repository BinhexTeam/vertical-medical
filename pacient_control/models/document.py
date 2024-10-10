from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AnalysisDocument(models.Model):
    _inherit = "dms.file"

    task_id = fields.Many2one(
        "project.task", string=_("Analysis")
    )  # A document can belong to a task (Mainly for analysis task)
