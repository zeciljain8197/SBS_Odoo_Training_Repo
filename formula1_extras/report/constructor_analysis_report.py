from odoo import models, fields, api, tools


class ConstructorAnalysis(models.Model):
    _inherit = 'constructor.analysis'

    wins = fields.Integer('No. of Wins')
    entry_fees = fields.Float('EntryFees', digits=(16, 3), help="Enter Constructor entry-fees!")
    fan_name = fields.Char("Top Fan's Name", size=64, required=True, help="Enter the Top fan's name!")

    def init(self):
        """
        Inherited init method to add additional fields to the existing view
        -------------------------------------------------------------------
        :return:
        """
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW constructor_analysis AS(
            SELECT c.id,
                   c.name constructor_name,
                   f.d_id,
                   c.engine,
                   c.t_3,
                   c.wins,
                   c.entry_fees,
                   f.fan_name
                   FROM formula1_constructors c, formula1_fans f 
                   WHERE c.driver_id = f.d_id)""")
