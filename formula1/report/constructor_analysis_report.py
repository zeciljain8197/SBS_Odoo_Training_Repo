from odoo import models, fields, tools


# Ex 8 Ques 1
class ConstructorAnalysis(models.Model):
    _name = 'constructor.analysis'
    _auto = False

    constructor_name = fields.Char('Constructor Name')
    d_id = fields.Many2one('formula1.driver', 'Driver Name')
    engine = fields.Selection(
        selection=[('redbull', 'Redbull'), ('mercedes', 'Mercedes'), ('ferrari', 'Ferrari'), ('renault', 'Renault')],
        string='Engine')
    t_3 = fields.Integer('Total Fandom %')

    def init(self):
        """
        This is an init method to create a view in PSQL
        :return: Created View
        """
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW constructor_analysis AS(
            SELECT c.id,
                   c.name constructor_name,
                   f.d_id,
                   c.engine,
                   c.t_3
                   FROM formula1_constructors c, formula1_fans f 
                   WHERE c.driver_id = f.d_id)""")
