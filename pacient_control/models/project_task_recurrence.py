# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import pytz
from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError

class ProjectTask(models.Model):
    _inherit = "project.task.recurrence"

    @api.model
    def _get_recurring_fields(self):
        # Add fields to recurring tasks
        return [
            "allowed_user_ids",
            "company_id",
            "description",
            "displayed_image_id",
            "email_cc",
            "parent_id",
            "partner_email",
            "partner_id",
            "partner_phone",
            "planned_hours",
            "project_id",
            "project_privacy_visibility",
            "sequence",
            "tag_ids",
            "recurrence_id",
            "name",
            "recurring_task",
            "tasktype_id",
            "product_event_ids",
            "app_selection_id",
            "app_partner_id",
        ]