from odoo import models, fields


class UpdateCircuitCost(models.TransientModel):
    _name = 'update.circuit.cost'
    _description = 'Update Circuit Cost'

    c_id = fields.Many2one('formula1.circuit', string='Circuit name')
    const_cost = fields.Integer('Construction Costs', group_operator='max')

    def update_circuit_cost(self):
        """
        This is a method to Update Circuit Cost
        -----------------------------------------
        :param self: object pointer
        """
        const = self.c_id
        if not const.ids:
            const_ids = self._context.get('active_ids')
            const_obj = self.env[self._context.get('active_model')]
            const = const_obj.browse(const_ids)
        const.write({
            'const_cost': self.const_cost,
        })
