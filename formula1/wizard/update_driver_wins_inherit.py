from odoo import fields, models

# from Odoo.projects.formula1.wizard import update_driver_wins


# Ex 7 Ques 11
# Ex 7 Ques 12
class UpdateDriverInherit(models.TransientModel):
    _inherit = 'update.driver.wins'

    d_podiums = fields.Integer('No of Podiums')

    def update_driver_wins(self):
        """
        Overridden method to update driver elements
        :param self: object pointer
        """
        d_win = self.d_id
        if not d_win.ids:
            d_win_ids = self._context.get('active_ids')
            d_win_obj = self.env[self._context.get('active_model')]
            d_win = d_win_obj.browse(d_win_ids)
        d_win.write({
            'd_podiums': self.d_podiums,
        })
        return super().update_driver_wins()
