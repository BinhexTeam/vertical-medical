# -*- coding: utf-8 -*-
# from odoo import http


# class BinhexEmployeeResidence(http.Controller):
#     @http.route('/employee_residence/employee_residence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_residence/employee_residence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_residence.listing', {
#             'root': '/employee_residence/employee_residence',
#             'objects': http.request.env['employee_residence.employee_residence'].search([]),
#         })

#     @http.route('/employee_residence/employee_residence/objects/<model("employee_residence.employee_residence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_residence.object', {
#             'object': obj
#         })
