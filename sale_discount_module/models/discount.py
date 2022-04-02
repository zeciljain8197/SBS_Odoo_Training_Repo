from odoo import models, fields, api


class SalesDiscount(models.Model):
    _inherit = 'sale.order.line'

    # Ex 6 Ques 9
    d_amnt = fields.Float("Discount Amount", compute='_calc_d_amnt')

    # Ex 6 Ques 10
    @api.depends('price_unit', 'discount')
    def _calc_d_amnt(self):
        for amnt in self:
            amnt.d_amnt = (amnt.price_unit * amnt.discount) / 100
