# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, tools, _
import logging
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)
        if res.has_group("residence_management.group_residence_admin"):
            # If user has admin group add him to all residences project
            residences = self.env["rm.residence"].search([])
            for resi in residences:
                for project in resi.project_ids:
                    project.write({"allowed_internal_user_ids": [(4, res.id)]})
        return res

    def write(self, vals):
        res = super().write(vals)
        if self.has_group("residence_management.group_residence_admin"):
            # If user has admin group add him to all residences project (if something is modified)
            residences = self.env["rm.residence"].search([])
            for resi in residences:
                for project in resi.project_ids:
                    project.write({"allowed_internal_user_ids": [(4, self.id)]})
        return res