from odoo import fields, models


# Ex 7 Ques 4
class UpdateFans(models.TransientModel):
    _name = 'update.fans'
    _description = 'Fans Wizard'

    fan_id = fields.Integer("Top Fan's ID", help="Enter top fan's id!")
    name = fields.Char("Top Fan's Name", size=64, required=True, help="Enter the Top fan's name!")
    constr_name = fields.Many2one(comodel_name='formula1.constructors', string='Constructor Name', ondelete="set null")
    fan_h = fields.Float('Fan Height')
    fan_w = fields.Float('Fan Weight')
    fan_age = fields.Float('Fan Age')

    def update_fans(self):
        """
        Method to add records in the fans field of constructors model
        :param self: object pointer
        """
        fan_id = self.env['formula1.fans']
        fan_id.create({
            'fan_id': self.fan_id,
            'fan_name': self.name,
            'constr': self.constr_name.id,
            'fan_h': self.fan_h,
            'fan_w': self.fan_w,
            'fan_age': self.fan_age
        })
        fan_record = self.env['formula1.constructors']
        fan_record.write({
            'fan_ids': [(0, 0, fan_id.id)]
        })
