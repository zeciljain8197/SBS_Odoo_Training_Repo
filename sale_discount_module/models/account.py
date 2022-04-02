from odoo import models, fields, api


# Ex 6 Ques 11
class Invoice_move_line(models.Model):
    _inherit = 'account.move.line'

    d_amnt = fields.Float('Discount_amount', store=True, readonly=True)

    @api.onchange('discount', 'price_unit')
    def _calc_discount_amount(self):
        for order in self:
            order.d_amnt = (order.discount * order.price_unit) / 100

    # Ex 6 Ques 12
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('discount', 0):
                vals.update({
                    'd_amnt': vals['discount'] * vals['price_unit'] / 100.0
                })
        return super(Invoice_move_line, self).create(vals_list)

    def write(self, vals):
        for line in self:
            if vals.get('discount', 0):
                price_unit = vals.get('price_unit') and vals['price_unit'] or line.price_unit
                vals.update({
                    'd_amnt': price_unit * vals['discount'] / 100.0
                })
        return super().write(vals)
