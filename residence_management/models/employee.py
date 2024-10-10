from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class Employee(models.Model):
    _inherit = "hr.employee"

    residence_id = fields.Many2one("rm.residence", string=_("Residence"))
    residence_ids = fields.Many2many(comodel_name="rm.residence",
        relation="residence_employee_table_1",
        column1="res_id",
        column2="emp_id",
        string=_("Residences"))

    # Work location computed by residence location
    # work_location = fields.Char(compute="_compute_work_location", string = _('Work Location'))

    # @api.model
    # def create(self, vals):
    #     # If option selected, creates contact and user for the new employee
    #     if self.env.user.has_group("residence_management.group_employee"):
    #         employee_user = self.env["res.users"].create(
    #             {
    #                 "name": vals["name"],
    #                 "login": vals["work_email"],
    #                 "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
    #                 "image_1920": (
    #                     vals["image_1920"] if "image_1920" in vals else False
    #                 ),
    #             }
    #         )
    #         employee_user.partner_id.email = vals["work_email"]
    #         employee_user.partner_id.employee_residence_id = (
    #             vals["residence_id"] if "residence_id" in vals else False
    #         )
    #         employee = super().create(vals)
    #         employee.address_home_id = employee_user.partner_id.id
    #         employee.user_id = employee_user.id
    #         # Adds user to the project when he is assigned to the residence in creation
    #         if vals["residence_id"]:
    #             project = self.env["project.project"].search(
    #                 [("residence_id", "=", vals["residence_id"])]
    #             )
    #             if project and employee_user:
    #                 project.write(
    #                     {"allowed_internal_user_ids": [(4, employee_user.id)]}
    #                 )
    #     else:
    #         employee = super().create(vals)
    #     return employee

    # def write(self, vals):
    #     for record in self:
    #         if self.env.user.has_group("residence_management.group_employee"):
    #             if "work_email" in vals:
    #                 record.address_home_id.email = vals["work_email"]
    #             if "residence_id" in vals:
    #                 # If residence is modified on employee, user's project permission also changes
    #                 record.address_home_id.employee_residence_id = vals["residence_id"]
    #                 old_project = self.env["project.project"].search(
    #                     [("residence_id", "=", record.residence_id.id)]
    #                 )
    #                 new_project = self.env["project.project"].search(
    #                     [("residence_id", "=", vals["residence_id"])]
    #                 )
    #                 if record.user_id:
    #                     if old_project:
    #                         old_project.write(
    #                             {"allowed_internal_user_ids": [(3, record.user_id.id)]}
    #                         )
    #                     if new_project:
    #                         new_project.write(
    #                             {"allowed_internal_user_ids": [(4, record.user_id.id)]}
    #                         )
    #             if "name" in vals:
    #                 record.address_home_id.name = vals["name"]

    #     employee = super().write(vals)
    #     return employee

    def action_document_through_contact(self):
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
        }


class EmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    residence_id = fields.Many2one("rm.residence")
