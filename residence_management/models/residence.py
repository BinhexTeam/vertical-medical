# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import re
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

import datetime


class Residence(models.Model):
    _name = "rm.residence"
    _description = "Residence"

    directory_ids = fields.One2many("dms.directory", "residence_id")

    # Fields

    name = fields.Char(string=_("Name"), required=True)
    description = fields.Text(string=_("Description"))
    image = fields.Binary(string=_("Image"))

    # Location

    street = fields.Char()
    zip_code = fields.Char(change_default=True)
    town = fields.Char()
    state_id = fields.Many2one(
        "res.country.state",
        string=_("State"),
        domain="[('country_id', '=?', country_id)]",
    )
    country_id = fields.Many2one("res.country", string=_("Country"))

    manager = fields.Many2one("hr.employee", string=_("Manager"))

    phone_num = fields.Char(string=_("Phone Number"))
    email = fields.Char(string=_("Email"))

    # Relations

    type_id = fields.Many2one("rm.residence.type", string=_("Type"))
    image_ids = fields.One2many("rm.image", "residence_id", string=_("Images"))
    resident_ids = fields.One2many("res.partner", "residence_id", string=_("Resident"))
    employee_resident_ids = fields.One2many(
        "res.partner", "employee_residence_id", string=_("Resident")
    )

    expense_ids = fields.One2many("hr.expense", "residence_id", string=_("Expenses"))
    journal_ids = fields.One2many(
        "account.journal", "residence_id", string=_("Journals")
    )

    room_ids = fields.One2many("rm.residence.room", "residence_id", string=_("Rooms"))

    employee_ids = fields.Many2many(comodel_name="hr.employee",
        relation="residence_employee_table_1",
        column1="emp_id",
        column2="res_id",
        string=_("Employees"))
    public_employees = fields.One2many(
        "hr.employee.public", "residence_id", string=_("Employees")
    )

    employee_contact_ids = fields.One2many(
        "res.partner", "employee_residence_id", string=_("Employees")
    )
    recruitment_ids = fields.One2many(
        "hr.applicant", "residence_id", string=_("Recruitments")
    )

    project_ids = fields.One2many(
        "project.project", "residence_id", string=_("Projects")
    )

    ticket_ids = fields.One2many("helpdesk.ticket", "residence_id", string=_("Tickets"))

    @api.onchange("email")
    def validate_mail(self):
        if self.email:
            match = re.match(
                "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                self.email,
            )
            if match == None:
                raise ValidationError(_("Not a valid E-mail"))

    # @api.onchange("manager")
    # def add_employee_residence(self):
    #     # When employee is added as manager, employee gets residence assigned
    #     if self.manager and not self.manager.residence_id:
    #         self.manager.residence_id = self._origin.id

    @api.model
    def create(self, vals):
        res = super(Residence, self).create(vals)

        # Adding users to residence project
        employee_users = self.env["res.users"].search(
            [
                "|",
                ("employee_id", "in", res.employee_ids.ids),
                (
                    "groups_id",
                    "in",
                    self.env.ref("residence_management.group_residence_admin").id,
                ),
            ]
        )

        # Look for project with same name
        project = self.env["project.project"].search(
            ["&", ("name", "=", res.name), ("residence_id", "=", False)], limit=1
        )

        # If project exists asign it to residence
        if project.name == False:
            project = self.env["project.project"].create(
                {
                    "name": res.name,
                    "privacy_visibility": "followers",
                    "allowed_internal_user_ids": [(6, 0, employee_users.ids)]
                    if employee_users
                    else False,
                }
            )
        res.project_ids = [(6, 0, [project.id])]

        # Add stages to the project
        stages = self.env["project.task.type"].search([])
        for stage in stages:
            stage.project_ids = [(4, project.id)]

        # Create document workspace for residence
        if res.name != _("Residents") and res.name != _("Employees"):
            directory_ids = self.env["dms.directory"].search([("name", "=", res.name)])
            parent_R = self.env.ref(
                "residence_management.documents_residents_folder"
            ).id
            parent_E = self.env.ref(
                "residence_management.documents_employees_folder"
            ).id
            # Assign folders for residence
            if len(directory_ids) == 0:
                residents_folder = self.env["dms.directory"].create(
                    {
                        "name": res.name,
                        "parent_id": parent_R,
                        "residence_id": res.id,
                        'is_root_directory': False
                    }
                )
                employees_folder = self.env["dms.directory"].create(
                    {
                        "name": res.name,
                        "parent_id": parent_E,
                        "residence_id": res.id,
                        'is_root_directory': False
                    }
                )

                # def _create_directory_vals(self, record):
                # return {
                #     "storage_id": self.storage.id,
                #     "is_root_directory": True,
                #     "name": record.display_name,
                #     "res_model": record._name,
                #     "res_id": record.id,
                # }

        return res

    def write(self, vals):
        res = super(Residence, self).write(vals)

        if vals.get("name"):

            # Change project and folder name

            [x.write({"name": vals["name"]}) for x in self.project_ids]

            directory_ids = self.env["dms.directory"].search([("name", "=", self.name)])
            if directory_ids:
                for folder in directory_ids:
                    folder.write({"name": vals["name"]})
            else:
                parent_R = self.env.ref(
                    "residence_management.documents_residents_folder"
                ).id
                parent_E = self.env.ref(
                    "residence_management.documents_employees_folder"
                ).id
                if len(directory_ids) == 0:
                    residents_folder = self.env["dms.directory"].create(
                        {"name": vals["name"], "parent_id": parent_R}
                    )
                    employees_folder = self.env["dms.directory"].create(
                        {"name": vals["name"], "parent_id": parent_E}
                    )

        return res

    def action_see_expenses(self):
        self.ensure_one()
        return {
            "name": _("Expenses"),
            "res_model": "hr.expense",
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "domain": [("residence_id", "=", self.id)],
            "context": "{'default_residence_id': "
            + str(self.id)
            + ", 'group_by': 'department_id'}",
        }

    def action_see_residents(self):
        self.ensure_one()

        return {
            "name": _("Residents"),
            "res_model": "res.partner",
            "type": "ir.actions.act_window",
            "view_mode": "kanban,form",
            "views": [
                (self.env.ref("residence_management.view_pacient_kanban").id, "kanban"),
                (False, "tree"),
                (self.env.ref("residence_management.view_pacient_form").id, "form"),
            ],
            "domain": [("residence_id", "=", self.id)],
            "context": "{'default_type': 'contact', 'default_residence_id': "
            + str(self.id)
            + "}",
        }

    def action_see_journals(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Journals"),
            "view_mode": "tree,form",
            "res_model": "account.journal",
            "domain": [("residence_id", "=", self.id)],
            "context": "{'default_residence_id': "
            + str(self.id)
            + ", 'default_type': 'bank'}",
        }

    def action_see_project(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Activities"),
            "view_mode": "kanban,form",
            #'view_id': self.env.ref('project.view_project_kanban').id,
            #'res_model': 'project.project',
            #'domain': [('residence_id', '=', self.id)],
            "res_model": "project.task",
            "domain": [("project_id.name", "=", self.name)],
            "context": "{'residence': True, 'default_project_id': "
            + str(self.sudo().project_ids[0].id)
            + "}",
        }


class Workspace(models.Model):
    _inherit = "dms.directory"

    residence_id = fields.Many2one("rm.residence")

    @api.onchange("residence_id")
    def change_name(self):
        self.name = self.residence_id.name
