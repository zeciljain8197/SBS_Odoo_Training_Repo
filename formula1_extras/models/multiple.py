from odoo import fields, models


# Ex 6 Ques 14
class MultipleInheritance(models.Model):
    _name = "multiple.inheritance"
    _inherit = ['formula1.fans', 'formula1.circuit']
    _description = 'Multiple inheritance'

    v_date = fields.Datetime('Visit Date')
    visited = fields.Selection(
        selection=[('yt', 'Yet to Visit'), ('vtw', 'Visiting this Weekend'), ('av', 'Already visited')],
        string='Visit Info')
    visit_review = fields.Boolean('Was Visit Satisfactory?')

