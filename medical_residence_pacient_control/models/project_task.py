# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
import pytz
from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, UserError

class AppointmentSelection(models.Model):
    _name = "rm.project.task.app.selection"
    _description = "Appointment Selections"
    name = fields.Char(translate=True)
    task_ids = fields.One2many("project.task", "app_selection_id")

class ProjectTask(models.Model):
    _inherit = "project.task"
    tasktype_id = fields.Many2one("project.task.tasktype", string=_("Task Type"))
    app_selection_id = fields.Many2one(
        "rm.project.task.app.selection", string=_("Appointment Type")
    )
    app_partner_id = fields.Many2one("res.partner", string=_("Appointment Partner"))
    document_ids = fields.One2many("dms.file", "task_id", string=_("Analysis Document"))
    product_event_ids = fields.Many2many(
        "product.template",
        string=_("Medicines"),
        domain=lambda self: [
            "|",
            ("categ_id", "in", self.env.user.company_id.category_med_ids.ids),
            ("categ_id", "in", self.env.user.company_id.category_vac_ids.ids),
        ],
    )
    control_hygiene_ids = fields.One2many(
        "rm.resident.control.hygiene.element", "task_id", string=_("Hygiene Events")
    )
    project_name = fields.Char(related="project_id.name")
    residence_id_task = fields.Integer(related="project_id.residence_id.id")
    # Document for analysis task
    directory_id = fields.Many2one(
        "dms.directory", compute="get_folder", store=True, string=_("Workspace")
    )
    tag_id = fields.Many2one("dms.tag", compute="get_tag", store=True, string=_("Tag"))


    @api.depends("partner_id")
    def get_folder(self):
        folder = (
            self.env["dms.directory"]
            .sudo()
            .search(
                [
                    "&",
                    ("name", "in", self.partner_id.residence_id.mapped('name')),
                    (
                        "parent_id",
                        "=",
                        self.env.ref(
                            "medical_residence_base.documents_residents_folder"
                        ).id,
                    ),
                ]
            )
        )
        if folder:
            self.directory_id = fields.first(folder).id
        else:
            self.directory_id = False

    @api.depends("directory_id")
    def get_tag(self):
        tag = (
            self.env["dms.tag"]
            .sudo()
            .search(
                [
                    (
                        "id",
                        "=",
                        self.env.ref(
                            "medical_residence_base.documents_residents_documents_analitica"
                        ).id,
                    )
                ]
            )
        )
        self.tag_id = tag.id
    # ----------------------------------------------------------------------------------------------------------------
    @api.model
    def create(self, vals):
        # Todays date as default if is not set
        if "date_deadline" not in vals:
            vals["date_deadline"] = fields.Date.today()
        return super(ProjectTask, self).create(vals)

    def send_mail(self):
        followers = self.message_follower_ids
        template_id = self.env.ref("medical_residence_pacient_control.email_template").id
        task = self.tasktype_id.name

    @api.onchange("product_event_ids")
    def control_resident_treatment(self):
        # Checks if pacient has treatment for current task medicines selected
        if self.partner_id:
            active_treatments = self.env["rm.resident.treatment"].search(
                [
                    ("resident_id", "=", self.partner_id.id),
                    ("active_treatment", "=", True),
                ]
            )
            treatment_products = []
            for t in active_treatments:
                for prod in t.product_ids:
                    treatment_products.append(prod.id)
            for prod in self.product_event_ids.ids:
                if prod not in treatment_products:
                    raise UserError(
                        _(
                            "Medicine not in current pacient treatments, please create a treatment first"
                        )
                    )

    @api.onchange("tasktype_id")
    def hygiene_events(self):
        # Ads hygiene elements by default
        if self.tasktype_id == self.env.ref("medical_residence_pacient_control.H_type"):
            elem_1 = self.env["rm.resident.control.hygiene.element"].create(
                {"name_id": self.env.ref("medical_residence_pacient_control.hygiene_elem_shower").id}
            )
            elem_2 = self.env["rm.resident.control.hygiene.element"].create(
                {"name_id": self.env.ref("medical_residence_pacient_control.hygiene_elem_shave").id}
            )
            elem_3 = self.env["rm.resident.control.hygiene.element"].create(
                {"name_id": self.env.ref("medical_residence_pacient_control.hygiene_elem_teeth").id}
            )

            self.control_hygiene_ids = [(6, 0, [elem_1.id, elem_2.id, elem_3.id])]

    # Basic control fields for task
    #weight = fields.Float(string=_("Weight"))
    #height = fields.Float(string=_("Height (meters)"))
    imc = fields.Float(compute="compute_imc", string=_("IMC"))

    heartbeat = fields.Integer(string=_("Heartbeat in 30s"))
    pressure = fields.Integer(compute="compute_beat", string=_("Pressure"))

    period_cicle_start = fields.Date(string=_("Period Cicle start"))
    period_cicle_end = fields.Date(string=_("Period Cicle end"))
    num_days = fields.Char(compute="num_days_", string=_("Period Cicle"))

    res_gender = fields.Selection(related="partner_id.gender", string=_("Gender"))


    # Control basico
    systolic_pressure = fields.Float(string=_("Systolic Pressure"))
    diastolic_pressure = fields.Float(string=_("Diastolic Pressure"))
    heart_rate = fields.Float(string=_("Heart Rate"))

    # Control saturacion
    saturation = fields.Integer(string=_("Saturation"))

    # Control peso
    weight = fields.Float(string=_("Weight"))

    # Control de glucemia
    glucose = fields.Float(string=_("Glucose"))

    # Control de altura
    height = fields.Float(string=_("Height"))
    temperature = fields.Float(string=_("Temperature"))
    
    # Control de deposiciones
    bowel_movement = fields.Selection([("normal", _("Normal")), ("hard", _("Hard")), ("soft", _("Soft"))], string=_("Bowel Movement"))

    # Menstruacion
    menstruation_start = fields.Date(string=_("Menstruation Start"))
    menstruation_end = fields.Date(string=_("Menstruation End"))

    @api.depends("height", "weight")
    def compute_imc(self):
        for record in self:
            if record.height > 0:
                record.imc = record.weight / (record.height * record.height)
            else:
                record.imc = 0

    @api.depends("heartbeat")
    def compute_beat(self):
        for record in self:
            if record.heartbeat > 0:
                record.pressure = record.heartbeat * 2
            else:
                record.pressure = 0

    @api.depends("period_cicle_start", "period_cicle_end")
    def num_days_(self):
        for record in self:
            if record.period_cicle_end and record.period_cicle_start:
                if record.period_cicle_start > record.period_cicle_end:
                    raise ValidationError(
                        _("Start date should not greater than end date.")
                    )
                else:
                    record.num_days = (
                        record.period_cicle_end - record.period_cicle_start
                    ).days
            else:
                record.num_days = 0

class HygieneElement(models.Model):
    _name = "rm.resident.control.hygiene.element"
    _description = "Hygiene Element"

    name_id = fields.Many2one(
        "rm.resident.control.hygiene.element.name", string=_("Nombre")
    )
    time = fields.Char(string=_("Time"))
    observations = fields.Char(string=_("Observations"))
    check = fields.Boolean(string=_("Done"))
    task_id = fields.Many2one("project.task", string=_("Task"))

class HygieneName(models.Model):
    _name = "rm.resident.control.hygiene.element.name"
    _description = "Hygiene Name"

    name = fields.Char(translate=True)
    element_ids = fields.One2many("rm.resident.control.hygiene.element", "name_id")

class TaskType(models.Model):
    _name = "project.task.tasktype"
    _description = "Project Task Type"

    name = fields.Char(string=_("Name"), translate=True)
    project_ids = fields.One2many("project.task", "tasktype_id", string=_("Project"))
