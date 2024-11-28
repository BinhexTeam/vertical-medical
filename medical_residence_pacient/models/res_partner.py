# Copyright 2024 Binhex - Zuzanna Elzbieta Szalaty Szalaty.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class Resident(models.Model):
    _inherit = "res.partner"

    identification_type = fields.Selection(
        [("dni", "DNI"), ("nie", "NIE"), ("passport", "Passport")],
        string=_("Identification Type"),
        default="dni",
        required=True,
        tracking=True
    )
    identification = fields.Char(string=_("Identification"), 
                                 required=True, 
                                 size=9,
                                 tracking=True
                                 )
    gender = fields.Selection(
        selection=[("ma", "Male"), ("fe", "Female"), ("ot", "Other")],
        string=_("Gender"),
        required=True,
        default='ma',
        tracking=True
    )
    marital_status = fields.Selection(
        [
            ("single", "Single"),
            ("married", "Married"),
            ("judicially_separated", "Judicially Separated"),
            ("divorced", "Divorced"),
            ("widower", "Widower"),
        ],
        string=_("Marital Status"),
        tracking=True
    )

    date_ingress = fields.Date(string=_("Date of Admission"),
                               tracking=True)

    age = fields.Integer(string="Age", 
                        compute="compute_age",
                        tracking=True
                         )

    # Contacts
    is_family = fields.Boolean(string=_("Resident Familiar"), tracking=True)
    relationship_ids = fields.One2many(
        "rm.resident.relationship", 
        "partner_id", 
        string="Relationship",
        tracking=True
    )
    family_contacts = fields.Many2many(
        "res.partner",
        "related_contact_fam",
        "fam_contact1",
        "fam_contact2",
        string="Family Contacts",
        tracking=True
    )
    observations = fields.Text(string=_("Observations"), tracking=True)
    # Documents
    document_ids = fields.One2many("dms.file", "resident_id_doc", string=_("Document"), tracking=True)

    # Account
    health_card = fields.Char(string=_("Health Card"),tracking=True)
    social_security_number = fields.Char(string=_("Social Security Number"),
                                         tracking=True)
    csv_number = fields.Char(string=_("CSV Number"),
                             tracking=True)
    pension_account_number = fields.Char(string=_("Pension Account Number"),
                                        tracking=True)
    responsible_account_number = fields.Char(string=_("Responsible Account Number"),
                                            tracking=True)
    systolic_pressure = fields.Float(
        string="Systolic Pressure"
    )
    diastolic_pressure = fields.Float(
        string="Diastolic pressure"
    )
    pulse = fields.Float(
        string="Pulse"
    )
    saturation = fields.Integer(
        string="Saturation"
    )
    weight = fields.Float(
        string="Weight"
    )
    blood_glucose = fields.Float(
        string="Blood glucose"
    )
    height = fields.Integer(
        string="Height"
        )
    temperature = fields.Float(
        string="Temperature"
        )
    
    # Calculate age
    @api.depends("date")
    def compute_age(self):
        for record in self:
            today_date = fields.Date.today()
            delta = relativedelta(today_date, record.date)
            record.age = delta.years

    @api.constrains("date_ingress")
    def _check_date_ingress(self):
        for record in self:
            if not record.residence_id and record.date_ingress:
                raise ValidationError(
                    _("Choose a residence before assigning a date of admission")
                )

    @api.onchange("is_family")
    def change_family_state(self):
        if self.is_family == True:
            self.residence_id = False

    def action_view_dms(self):
        action = self.env["ir.actions.act_window"]._for_xml_id("dms.action_dms_file")
        directory_id = False
        folder = self.env["dms.directory"].sudo().search([])
        for fold in folder:
            if fold.name == self.residence_id.name:
                directory_id = fold.id
                
        action["domain"] = str(
            [
                ("partner_id", "=", self.id),
            ]
        )
        action["context"] = str(
            {
                "default_partner_id": self.id,
                "default_resident_id_doc": self.id,
                "default_directory_id": directory_id,
            }    
        )
        return action

    document_count = fields.Integer("Document Count", compute="_compute_document_count")

    def _compute_document_count(self):
        read_group_var = self.env["dms.file"].read_group(
            [("partner_id", "in", self.ids)],
            fields=["partner_id"],
            groupby=["partner_id"],
        )

        document_count_dict = dict(
            (d["partner_id"][0], d["partner_id_count"]) for d in read_group_var
        )
        for record in self:
            record.document_count = document_count_dict.get(record.id, 0)


class RelationshipType(models.Model):
    _name="rm.resident.relationship.type"
    _description = "type of relationship"
    _sql_constraints =  [('unique_name', 'UNIQUE(name)', _('It already exists a type with that name.'))]
    
    name = fields.Char(
        string='Name',
        required=True,
        translate=True
        )

class RelationshipType(models.Model):
    _name="rm.resident.relationship.legal"
    _description = "legal relation of relationship"
    _sql_constraints =  [('unique_name', 'UNIQUE(name)', _('It already exists a legal relation with that name.'))]
    
    name = fields.Char(
        string='Name',
        required=True,
        translate=True
        )
    


class Relationship(models.Model):
    _name = "rm.resident.relationship"
    _description = "Resident Relationship"

    name = fields.Char(compute="get_Name", 
                       string=_("Name"),
                       tracking=True)
    relation_name = fields.Many2one(
        comodel_name="rm.resident.relationship.type", 
        string=_("Relation")
    )
    relation_legal_id = fields.Many2one(comodel_name="rm.resident.relationship.legal", string="Legal relation")
    partner_id = fields.Many2one("res.partner", string=_("Partner"),tracking=True)
    family_partner = fields.Many2one("res.partner", 
                                     string=_("Relative"), 
                                     required=True, 
                                     tracking=True)
    family_partner_num = fields.Char(string=_("Phone"), 
                                    related="family_partner.mobile", 
                                    tracking=True)

    @api.depends("relation_name", "family_partner")
    def get_Name(self):
        for record in self:
            if record.relation_name and record.family_partner:
                record.name = (
                    record.family_partner.name + " (" + record.relation_name.name + ")"
                )
            else:
                record.name = False

    def create(self, vals):
        res = super(Relationship, self).create(vals)
        for new_val in vals:
            if "family_partner" in new_val and "family_partner_num" in new_val:
                partner_id = self.env["res.partner"].browse(new_val["family_partner"])
                partner_id.mobile = new_val["family_partner_num"]
        for record in res:
            record.family_partner.write(
                {"family_contacts": [(4, record.partner_id.id)]}
            )
        return res

    def write(self, vals):
        if "family_partner_num" in vals:
            partner_id = (
                self.env["res.partner"].browse(vals["family_partner"])
                if "family_partner" in vals
                else self.family_partner
            )
            partner_id.mobile = vals["family_partner_num"]
        # Modify relationship when changing family
        if "family_partner" in vals:
            self.family_partner.write({"family_contacts": [(3, self.partner_id.id)]})
            self.env["res.partner"].browse(vals["family_partner"]).write(
                {"family_contacts": [(4, self.partner_id.id)]}
            )
        return super(Relationship, self).write(vals)

    def unlink(self):
        for record in self:
            record.family_partner.write(
                {"family_contacts": [(3, record.partner_id.id)]}
            )
        return super(Relationship, self).unlink()
