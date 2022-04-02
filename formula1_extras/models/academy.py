from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class Academy(models.Model):
    _inherit = ['formula1.constructors']

    a_exist = fields.Boolean('Constructor Has Academy or Not')
    # ad_name = fields.One2many('formula1.driver', '', 'Academy Driver Names')
    awards = fields.Selection(
        selection=[('ps', 'Fastest Pit Stop'), ('lt', 'Fastest Lap Time'), ('dod', 'Driver Of the Day'),
                   ('mo', 'Most Overtakes')])
    a_no = fields.Integer('No of Supporting Academies')
    extra_teams_ids = fields.Many2many('formula1.extras.teams', 'formula1_constructors_formula1_extras_teams_rel',
                                       'const_id', 'team_id', 'Academy Name')
    a_notes = fields.Char('Extra Notes Regarding Academies')
    # Ex 6 Ques 4
    test_str = fields.Datetime('Team testing session start', default=datetime.now())
    part_ids = fields.Many2many('formula1.part', 'formula1_part_formula1_constructors_rel1', 'part_id', 'const_id',
                                'Parts Supplier')

    # Ex 6 Ques 6
    @api.constrains('email')
    def check_c_code(self):
        """
        Check age based on the dob
        --------------------------
        :param self: object pointer
        """
        for const in self:
            if len(const.email) < 7:
                raise ValidationError('Email is too short to be valid!')

    # Ex 6 Ques 7
    def button_for_env(self):
        """
        This method is defined to compute results of environment methods.
        ---------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        super().button_for_env()
        print("New line added for Ex 6 Ques 7")


class AcademyTeams(models.Model):
    _name = "formula1.extras.teams"
    _description = "Academy Teams"
    _rec_name = "a_name"

    a_name = fields.Char('Academy Team Name', required=True)
    a_series = fields.Selection(
        selection=[('f2', 'Formula2'), ('f3', 'Formula3'), ('ic', 'IndyCar'), ('fE', 'FormulaE')],
        string="Team Competing In")


class Driver(models.Model):
    _inherit = "formula1.driver"

    d_state = fields.Selection(
        selection=[('d1', 'Legendary'), ('d2', 'Veteran'), ('d3', 'Title Competitor'), ('d4', 'Experienced'),
                   ('d5', 'Rookie'), ('d6', 'Academy Driver')], string='Experience', copy=False)

    def button_for_state(self):

        for state in self:
            if state.d_state != 'd6':
                state.d_state = 'd6'

    # Ex 6 Ques 5
    @api.onchange('d_state')
    def onchange_state(self):
        """
        Onchange method to set salary based on driver experience
        -------------------------------------------
        :param self: object pointer
        """
        super().onchange_state()
        for driver in self:
            if driver.d_state == 'd5':
                driver.d_wins = 0
