from odoo import fields, models, api


# Ex 7 Ques 1
class UpdateEntryFees(models.TransientModel):
    _name = 'update.entry.fees'
    _description = 'Entry Fees Wizard'

    const_id = fields.Many2one('formula1.constructors', string='Constructor')
    entry_fees_new = fields.Float('Updated Entry Fees')

    def update_rec(self):
        """
        Method to update entry fees in main model
        -----------------------------------------
        :param self: object pointer
        """
        const = self.const_id
        if not const.ids:
            const_ids = self._context.get('active_ids')
            const_var = self.env[self._context.get('active_model')]
            const = const_var.browse(const_ids)
        const.write({
            'entry_fees': self.entry_fees_new
        })
