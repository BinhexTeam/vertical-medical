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
        track_visibility='onchange'
    )
    identification = fields.Char(string=_("Identification"), 
                                 required=True, 
                                 size=9,
                                 track_visibility='onchange'
                                 )
    gender = fields.Selection(
        [("ma", "Male"), ("fe", "Female"), ("ot", "Other")],
        string=_("Gender"),
        required=True,
        track_visibility='onchange'
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
        track_visibility='onchange'
    )

    date_ingress = fields.Date(string=_("Date of Admission"),
                               track_visibility='onchange')

    age = fields.Integer(string="Age", 
                        compute="compute_age",
                        track_visibility='onchange'
                         )

    # Contacts
    is_family = fields.Boolean(string=_("Resident Familiar"), track_visibility='onchange')
    relationship_ids = fields.One2many(
        "rm.resident.relationship", 
        "partner_id", 
        string="Relationship",
        track_visibility='onchange'
    )
    family_contacts = fields.Many2many(
        "res.partner",
        "related_contact_fam",
        "fam_contact1",
        "fam_contact2",
        string="Family Contacts",
        track_visibility='onchange'
    )
    observations = fields.Text(string=_("Observations"), track_visibility='onchange')
    # Documents
    document_ids = fields.One2many("dms.file", "resident_id_doc", string=_("Document"), track_visibility='onchange')

    # Account
    health_card = fields.Char(string=_("Health Card"),track_visibility='onchange')
    social_security_number = fields.Char(string=_("Social Security Number"),
                                         track_visibility='onchange')
    csv_number = fields.Char(string=_("CSV Number"),
                             track_visibility='onchange')
    pension_account_number = fields.Char(string=_("Pension Account Number"),
                                        track_visibility='onchange')
    responsible_account_number = fields.Char(string=_("Responsible Account Number"),
                                             track_visibility='onchange')

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


class Relationship(models.Model):
    _name = "rm.resident.relationship"
    _description = "Resident Relationship"

    name = fields.Char(compute="get_Name", string=_("Name"),track_visibility='onchange')
    relation_name = fields.Char(string=_("Relation"),)
    partner_id = fields.Many2one("res.partner", string=_("Partner"),track_visibility='onchange')
    family_partner = fields.Many2one("res.partner", string=_("Relative"), required=True, track_visibility='onchange')
    family_partner_num = fields.Char(string=_("Phone"), related="family_partner.mobile", track_visibility='onchange')

    @api.depends("relation_name", "family_partner")
    def get_Name(self):
        for record in self:
            if record.relation_name and record.family_partner:
                record.name = (
                    record.family_partner.name + " (" + record.relation_name + ")"
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
