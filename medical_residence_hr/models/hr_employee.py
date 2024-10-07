from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = "hr.employee"

    residence_id = fields.Many2one("residence.residence", string=_("Residence"))
    residence_ids = fields.Many2many(comodel_name="residence.residence",
        relation="residence_employee_table_1",
        column1="res_id",
        column2="emp_id",
        string=_("Residences"))


    '''def action_document_through_contact(self):
        self.ensure_one()
        directory_id = False
        folder = self.env["dms.directory"].sudo().search([])
        for fold in folder:
            if fold.name in self.residence_ids.mapped('name') and fold.parent_id.name == _(
                "Employees"
            ):
                directory_id = fold.id
        return {
            "name": _("Documents"),
            "res_model": "dms.file",
            "type": "ir.actions.act_window",
            "view_mode": "kanban",
            "context": {
                "search_default_partner_id": self.address_home_id.id,
                "default_partner_id": self.address_home_id.id,
                "searchpanel_default_directory_id": directory_id,
            },
        }'''


class EmployeePublic(models.Model):
    _inherit = "hr.employee.public"
    residence_id = fields.Many2one("rm.residence")