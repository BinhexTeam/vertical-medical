# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class medical_residence_pacients(models.Model):
#     _name = 'medical_residence_pacients.medical_residence_pacients'
#     _description = 'medical_residence_pacients.medical_residence_pacients'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
