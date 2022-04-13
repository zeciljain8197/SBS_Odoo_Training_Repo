from odoo import fields, models


# Ex 7 Ques 9
class UpdateFansAlt(models.TransientModel):
    _name = 'update.fans.alt'
    _description = 'Update Fans Alt'

    c_id = fields.Many2one('formula1.constructors', string='Constructor')
    f_ids = fields.Many2many(comodel_name='formula1.fans', string='Fans')

    def update_fans_alt(self):
        """
        This method is used to update fans through constructors
        :param self: object pointer
        """
        for fan in self:
            fans = fan.f_ids
            print("Fans---------->", fans)
            if len(self.f_ids) == 1:
                action = {
                    'name': 'Fans 1',
                    'type': 'ir.actions.act_window',
                    'res_model': 'formula1.fans',
                    'view_mode': 'form',
                    'res_id': fans.ids[0],
                    'domain': [('id', 'in', fans.id)],
                }
                return action
            else:
                action = {
                    'name': 'Fans 2',
                    'type': 'ir.actions.act_window',
                    'res_model': 'formula1.fans',
                    'view_mode': 'tree,form',
                    'domain': [('id', 'in', fans.ids)],
                }
                return action
