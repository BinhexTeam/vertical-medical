# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = "project.project"