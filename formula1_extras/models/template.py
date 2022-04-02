from odoo import fields, models, api


# Ex 6 Ques 27
class ExtraCircuit(models.Model):
    _name = 'extra.circuit'
    _description = 'Extra circuit'
    _inherits = {'formula1.circuit': 'circuit_id'}
    _rec_name = 'extcir_name'

    extcir_name = fields.Char('Extra Circuit Name')
    main_cost = fields.Float('Maintenance Costs')
    circuit_id = fields.Many2one('formula1.circuit',
                                 'Circuits', required=True, ondelete='cascade')


# Ex 6 Ques 28
class ExtraParts(models.Model):
    _name = 'extra.part'
    _description = 'Extra Part Suppliers'
    _rec_name = 'p_name'

    p_name = fields.Char('Substitute part supplier')
    costly = fields.Boolean('Costly than the primary supplier?')
    efficient = fields.Boolean('Efficient than the primary supplier?')
    part_id = fields.Many2one('formula1.part', 'Primary Part Supplier', required=True, ondelete='cascade',
                              delegate=True)
