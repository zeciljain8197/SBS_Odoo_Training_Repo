from odoo import models, fields, api


class AadharPan(models.Model):
    _inherit = 'hr.employee'

    aadhar_no = fields.Char('Aadhar Number', size=12)
    pan_no = fields.Char('PAN', size=10)
