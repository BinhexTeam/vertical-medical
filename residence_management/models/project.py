from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = "project.project"

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
