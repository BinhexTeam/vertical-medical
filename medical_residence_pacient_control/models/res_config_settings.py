# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from odoo import fields, models, _

class Company(models.Model):
    _inherit = "res.company"
    # Categories for medicine and vaccine
    category_med_ids = fields.Many2many(
        "product.category",
        "category_med_ids_",
        string=_("Medicine categories"),
        default=lambda self: self.env.ref("medical_residence_pacient_control.med_prod_cat"),
    )
    category_vac_ids = fields.Many2many(
        "product.category",
        "category_vac_ids_",
        string=_("Vaccine categories"),
        default=lambda self: self.env.ref("medical_residence_pacient_control.vac_prod_cat"),
    )


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    group_categories_1 = fields.Boolean(
        string=_("Categories"),
        implied_group="medical_residence_pacient_control.group_categories_1",
        default=True,
    )
    medicine_category_ids = fields.Many2many(
        string=_("Medicine Categories"),
        related="company_id.category_med_ids",
        readonly=False,
    )
    vaccine_category_ids = fields.Many2many(
        string=_("Vaccine Categories"),
        related="company_id.category_vac_ids",
        readonly=False,
    )
