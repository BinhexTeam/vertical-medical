# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class Resident(models.Model):
    _inherit = "res.partner"
    
    date = fields.Date(string=_("Date"), track_visibility='onchange')
    street = fields.Char(string=_("Street"), track_visibility='onchange')
    street2 = fields.Char(string=_("Street2"), track_visibility='onchange')
    zip = fields.Char(string=_("Zip"), track_visibility='onchange')
    city = fields.Char(string=_("City"), track_visibility='onchange')
    state_id = fields.Many2one("res.country.state", string=_("State"), track_visibility='onchange')
    country_id = fields.Many2one("res.country", string=_("Country"), track_visibility='onchange')
    phone = fields.Char(string=_("Phone"), track_visibility='onchange')
    medical_info_ids = fields.One2many(
        "rm.resident.medical.info", "resident_id", string=_("Medical Info"),
        track_visibility='onchange'
    )
    medical_treatment_ids = fields.One2many(
        "rm.resident.treatment", "resident_id", string=_("Medical Treatment"),
        track_visibility='onchange'
    )
    task_appointment_id = fields.One2many(
        "project.task", "app_partner_id", string=_("Appointments"),
        track_visibility='onchange'
    )

    def action_see_basic_calendar(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Basic"),
            "view_mode": "calendar",
            "res_model": "project.task",
            "view_id": self.env.ref(
                "medical_residence_pacient_control.project_task_pacient_view_filtered"
            ).id,
            "domain": [
                "&",
                ("partner_id", "=", self.id),
                ("tasktype_id", "=", self.env.ref("medical_residence_pacient_control.BC_type").id),
            ],
            "context": {
                "default_project_id": self.sudo().residence_id.project_ids[0].id,
                "default_partner_id": self.id,
                "default_tasktype_id": self.env.ref("medical_residence_pacient_control.BC_type").id,
            },
        }

    def action_see_treatment(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Treatment"),
            "view_mode": "calendar",
            "res_model": "project.task",
            "domain": [
                "&",
                ("partner_id", "=", self.id),
                ("tasktype_id", "=", self.env.ref("medical_residence_pacient_control.T_type").id),
            ],
            "view_id": self.env.ref(
                "medical_residence_pacient_control.project_task_pacient_view_filtered"
            ).id,
            "context": {
                "default_project_id": self.sudo().residence_id.project_ids[0].id,
                "default_partner_id": self.id,
                "default_tasktype_id": self.env.ref("medical_residence_pacient_control.T_type").id,
            },
        }

    def action_see_analysis_calendar(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Analysis"),
            "view_mode": "calendar",
            "res_model": "project.task",
            "view_id": self.env.ref(
                "medical_residence_pacient_control.project_task_pacient_view_filtered"
            ).id,
            "domain": [
                "&",
                ("partner_id", "=", self.id),
                ("tasktype_id", "=", self.env.ref("medical_residence_pacient_control.A_type").id),
            ],
            "context": {
                "default_project_id": self.sudo().residence_id.project_ids[0].id,
                "default_partner_id": self.id,
                "default_tasktype_id": self.env.ref("medical_residence_pacient_control.A_type").id,
            },
        }

    def action_see_hygiene_calendar(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Hygiene"),
            "view_mode": "calendar",
            "res_model": "project.task",
            "view_id": self.env.ref(
                "medical_residence_pacient_control.project_task_pacient_view_filtered"
            ).id,
            "domain": [
                "&",
                ("partner_id", "=", self.id),
                ("tasktype_id", "=", self.env.ref("medical_residence_pacient_control.H_type").id),
            ],
            "context": {
                "default_project_id": self.sudo().residence_id.project_ids[0].id,
                "default_partner_id": self.id,
                "default_tasktype_id": self.env.ref("medical_residence_pacient_control.H_type").id,
            },
        }

    def action_see_tasks_calendar(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tasks"),
            "view_mode": "calendar",
            "res_model": "project.task",
            "view_id": self.env.ref("medical_residence_pacient_control.project_task_pacient_view").id,
            "domain": [("partner_id", "=", self.id)],
            "context": {
                "default_project_id": self.sudo().residence_id.project_ids[0].id,
                "create": 1,
                "edit": 1,
                "delete": 1,
                "default_partner_id": self.id,
            },
        }

    def action_see_tasks_monitoring(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tasks"),
            "view_mode": "calendar",
            "res_model": "project.task",
            "view_id": self.env.ref(
                "medical_residence_pacient_control.project_task_pacient_view_filtered"
            ).id,
            "domain": [
                "&",
                ("partner_id", "=", self.id),
                ("tasktype_id", "=", self.env.ref("medical_residence_pacient_control.M_type").id),
            ],
            "context": {
                "default_project_id": self.sudo().residence_id.project_ids[0].id,
                "default_partner_id": self.id,
                "default_tasktype_id": self.env.ref("medical_residence_pacient_control.M_type").id,
            },
        }
