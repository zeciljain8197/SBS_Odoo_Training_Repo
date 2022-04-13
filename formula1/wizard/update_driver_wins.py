from odoo import models, fields


class UpdateDriverWins(models.TransientModel):
    _name = 'update.driver.wins'
    _description = 'Update Driver Wins'

    d_id = fields.Many2one('formula1.driver', string='Driver Name')
    d_wins = fields.Integer('No of Wins')

    def update_driver_wins(self):
        """"
        This method is used to update driver wins
        -----------------------------------------
        :param self: object pointer
        """
        d_win = self.d_id
        if not d_win.ids:
            d_win_ids = self._context.get('active_ids')
            d_win_obj = self.env[self._context.get('active_model')]
            d_win = d_win_obj.browse(d_win_ids)
        d_win.write({
            'd_wins': self.d_wins,
        })
