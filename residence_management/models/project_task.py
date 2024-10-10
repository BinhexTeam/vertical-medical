# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _, SUPERUSER_ID
import re
from odoo.exceptions import ValidationError

class Project(models.Model):
    _inherit = "project.task"

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # Gets all task's stages when accesing from residence
        if "residence" in self.env.context:
            search_domain = []
            stage_ids = stages._search(
                search_domain, order=order, access_rights_uid=SUPERUSER_ID
            )
            return stages.browse(stage_ids)
        else:
            search_domain = [("id", "in", stages.ids)]
            if "default_project_id" in self.env.context:
                search_domain = [
                    "|",
                    ("project_ids", "=", self.env.context["default_project_id"]),
                ] + search_domain

            stage_ids = stages._search(
                search_domain, order=order, access_rights_uid=SUPERUSER_ID
            )
            return stages.browse(stage_ids)
