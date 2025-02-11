# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class docs(models.Model):
    _inherit = "dms.file"

    resident_id_doc = fields.Many2one("res.partner", string=_("Resident"))
    partner_id = fields.Many2one("res.partner", string="Contact", tracking=True)

    def default_directory_id(self):
        if "residence" in self.env.context:
            residence = self.env["rm.residence"].browse(self.env.context["residence"])
            if residence:
                folder = (
                    self.env["dms.directory"]
                    .sudo()
                    .search([("name", "=", residence.name)])
                )
                return folder
        else:
            return False

    directory_id = fields.Many2one(
        "dms.directory",
        string="Workspace",
        ondelete="restrict",
        tracking=True,
        required=False,
        index=True,
        default=default_directory_id,
    )
