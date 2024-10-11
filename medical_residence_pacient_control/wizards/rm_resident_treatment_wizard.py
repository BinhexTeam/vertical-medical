# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import models, fields, api, _

class CreateTreatment(models.TransientModel):
    _name = "rm.resident.treatment.wizard"
    _description = "Create Resident Treatment Wizard"

    name = fields.Char(string=_("Name"))
    date_begin = fields.Date(string=_("Initial Date"))
    date_end = fields.Date(string=_("End Date"))
    resident_id = fields.Many2one("res.partner", string=_("Resident"))
    product_ids = fields.Many2many(
        "product.template",
        string=_("Medicines"),
        domain=lambda self: [
            "|",
            ("categ_id", "in", self.env.user.company_id.category_med_ids.ids),
            ("categ_id", "in", self.env.user.company_id.category_vac_ids.ids),
        ],
    )

    def create_treatment(self):
        self.ensure_one()
        new_treatment = self.env["rm.resident.treatment"].create(
            {
                "name": self.name,
                "date_begin": self.date_begin,
                "date_end": self.date_end,
                "resident_id": self.resident_id.id,
                "product_ids": self.product_ids.ids,
            }
        )
