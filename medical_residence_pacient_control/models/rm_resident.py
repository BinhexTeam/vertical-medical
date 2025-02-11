# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MedicalInfoFields(models.Model):
    _name="rm.resident.medical.info.fields"
    _description="model for name medical info"
    _sql_constraints =  [('unique_name', 'unique(name)',_('It already exists a field with that name.'))]
    
    name = fields.Char(
        string="Name",
        translate=True,
        required=True
    )
    

class MedicalInfo(models.Model):
    _name = "rm.resident.medical.info"
    _description = "Previous medical information about the pacient"
   
    name = fields.Many2one(
        comodel_name="rm.resident.medical.info.fields",
        string="Field",
        required=True
    )
    observation = fields.Char(string=_("Observation"), tracking=True)
    resident_id = fields.Many2one("res.partner", string=_("Resident"))

class Treatment(models.Model):
    _name = "rm.resident.treatment"
    _order = "active_treatment desc, date_begin desc"
    _description = "Resident Treatment"

    name = fields.Char(string=_("Name"), tracking=True)
    resident_id = fields.Many2one("res.partner", string=_("Resident"), tracking=True)

    product_ids = fields.Many2many(
        "product.template",
        string=_("Medicines"),
        domain=lambda self: [
            "|",
            ("categ_id", "in", self.env.user.company_id.category_med_ids.ids),
            ("categ_id", "in", self.env.user.company_id.category_vac_ids.ids),
        ],
        tracking=True
    )

    @api.depends("date_begin", "date_end")
    def _compute_active_treatment(self):
        today = fields.Date.today()
        for record in self:
            if record.date_begin and record.date_end:
                if record.date_begin > record.date_end:
                    record.active_treatment = False
                    raise ValidationError(
                        _("Start date should not greater than end date.")
                    )
                else:
                    if today >= record.date_begin and today <= record.date_end:
                        record.active_treatment = True
                    else:
                        record.active_treatment = False
            elif record.date_begin and not record.date_end:
                if record.date_begin <= today:
                    record.active_treatment = True
            else:
                record.active_treatment = False

    active_treatment = fields.Boolean(
        string=_("Active"), compute=_compute_active_treatment, store=True
    )

    date_begin = fields.Date(string=_("Initial Date"))
    date_end = fields.Date(string=_("End Date"))

    def action_plan_activity(self):
        self.ensure_one()
        project = self.env["project.project"].search(
            [("residence_id", "=", self.resident_id.residence_id.id)]
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Treatment"),
            "view_mode": "form",
            "res_model": "project.task",
            "context": {
                "default_name": self.name,
                "default_partner_id": self.resident_id.id,
                "default_tasktype_id": self.env.ref("medical_residence_pacient_control.T_type").id,
                "default_product_event_ids": self.product_ids.ids,
                "dafault_user_id": self.env.user.id,
                "default_date_deadline": fields.Datetime.now(),
                "default_repeat_until": self.date_end,
                "default_project_id": project.id,
            },
        }
