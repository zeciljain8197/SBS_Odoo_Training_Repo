from odoo import models, fields


# Ex 7 Ques 6
class ViewConstr(models.TransientModel):
    _name = 'view.constr'
    _description = 'View constructors'

    driver_id = fields.Many2one(comodel_name='formula1.driver', string='Main Driver', ondelete="restrict")

    def view_constr(self):
        if self.driver_id.id == 1:
            action = self.env.ref('formula1.action_constructors_max').read()[0]
            return action
        elif self.driver_id.id == 2:
            action = self.env.ref('formula1.action_constructors_charles').read()[0]
            return action
        elif self.driver_id.id == 3:
            action = self.env.ref('formula1.action_constructors_jehan').read()[0]
            return action
