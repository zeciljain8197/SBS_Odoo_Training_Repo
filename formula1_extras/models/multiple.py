from odoo import fields, models


# Ex 6 Ques 14
class MultipleInheritance(models.Model):
    _name = "multiple.inheritance"
    _inherit = ['formula1.fans', 'formula1.circuit']
    _description = 'Multiple inheritance'

    v_date = fields.Datetime('Visit Date')
