# Importing the packages from odoo module
from odoo import models, fields, api
from datetime import datetime

# Creating a date value for using in the models
cr_dt = datetime.today()


# Creating a model of name:Constructors by creating its class
class Constructors(models.Model):
    # Defining model attributes
    _name = 'formula1.constructors'
    _description = 'Constructors'
    _table = 'formula1_constructors'
    _order = 'sequence'
    # Defining parent_name and parent_path for hierarchy of this model
    _parent_name = 'parent_id'
    _parent_store = True

    # Defining various fields of the model
    const_id = fields.Integer('Number', default=False, help="Enter Constructor Number!")
    name = fields.Char('Constructor Name', required=True, size=64, trim=True, help="Enter Constructor Name!")
    entry_fees = fields.Float('EntryFees', digits=(16, 3), help="Enter Constructor entry-fees!")
    active = fields.Boolean('Active', default=True, help="Enter Constructor active status!")
    const_notes = fields.Text('Constructor Notes', help="Enter any notes regarding the constructor!")
    driver1_notes = fields.Text('Driver1 Notes', help="Enter any notes regarding the drivers!")
    driver2_notes = fields.Text('Driver2 Notes', help="Enter any notes regarding the drivers!")
    html = fields.Html('Constructor Fanpage', help="Enter html!")
    st_date = fields.Datetime('Join Date', help="Enter Constructor start date!")
    nxt_date = fields.Date('Next Fanfest', default=cr_dt, help="Enter Constructor's next fanfest date'!")

    # Defining a selection field for drop down menu of various values to choose from! It will have a list of tuples
    engine = fields.Selection(
        selection=[('mercedes', 'Mercedes'), ('redbull', 'Redbull'), ('ferrari', 'Ferrari'),
                   ('porsche', 'Porsche')],
        string='Engine supplier', help="Enter Constructor Engine supplier!")
    test_entry = fields.Char('TestEntry', size=4, default="F1")
    password = fields.Char('Password')
    email = fields.Char('Email')
    webst = fields.Char('URL')

    # Defining a selection field to create a field having stars for priority/rating purposes!
    priority = fields.Selection([(str(ele), str(ele)) for ele in range(6)], 'Priority')
    sign_in = fields.Float('Sign In')
    sign_out = fields.Float('Sign Out')
    # Defining Relational fields
    driver_id = fields.Many2one(comodel_name='formula1.driver', string='Main Driver', ondelete="restrict")

    # For this O2M field we need a M2O field present in its comodel which will be used as inverse_name in O2M field.
    fan_ids = fields.One2many(comodel_name="formula1.fans", inverse_name="constr", string="Fans", limit=10)

    # For M2M fields we will need comodel, relation(1stmodel_2ndmodel_rel), col1, col2, string as attr
    fav_ids = fields.Many2many(comodel_name="formula1.circuit", string='Fav Circuits')
    part_ids = fields.Many2many('formula1.part', 'formula1_part_formula1_constructors_rel', 'part_id', 'const_id',
                                'Parts Supplier')

    # Defining a M2O field for currency having comodel-res.currency, fetching all available currencies from that model
    currency_id = fields.Many2one('res.currency', 'currency')

    # Defining Monetary field which is going to be used to select the currency to be selected!
    val = fields.Monetary(currency_field='currency_id', string='Valuation')

    # Defining a Reference field which works as a combination of Selection and M2O fields
    extra_info = fields.Reference(
        selection=[("formula1.driver", "Drivers"), ("formula1.fans", "Fans"), ("formula1.circuit", "Circuits")])

    # Defining fields for uploading Documents/Images on the server
    docu = fields.Binary('Constructor Info', help='Enter the constructor logo here!')
    img = fields.Image('Constructor Logo')

    # Defining a field for preserving the file name of the uploaded file
    file_name = fields.Char()

    # Defining fields where we will compute certain values automatically using compute attr and passing fn in them.
    t_1 = fields.Float('Fan Description 1', compute='_calc_fd_1')
    t_2 = fields.Float('Fan Description 2', compute='_calc_fd_2')
    t_3 = fields.Integer('Total Fandom %', compute='_calc_tf')
    state = fields.Selection(
        selection=[('s1', 'Established Team'), ('s2', 'Title Contender'), ('s3', 'Sister Team'), ('s4', 'Underdog'),
                   ('s5', 'New Entrant')], string='States')

    # Defining a field for giving sequencing feature to the tree view
    sequence = fields.Integer('Sequence')

    # Defining parent_id which will be a M2O field for giving hierarchy of the main model
    parent_id = fields.Many2one('formula1.constructors', string='Supplier Team')

    # Defining child_ids(O2M) for the respective parent_id(M2O) to create its child fields
    child_ids = fields.One2many('formula1.constructors', 'parent_id', string='Consumer Teams')

    # Defining a field parent_path which will be used to store the hierarchy of each field in the DB
    parent_path = fields.Char('parent_path')

    # Defining a decorator for all the functions to reflect any changes made to their values on runtime itself
    @api.onchange('fan_ids.fan_desc_1')
    def _calc_fd_1(self):
        """
        This method is defined to find fan description for main model.
        ---------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            for rr in record.fan_ids:
                record.t_1 += rr.fan_desc_1

    # The values which are passed in the decorator are the values that the fn depends on.
    # Means when those values are changed, the main value of the fn will also get changes accordingly.
    @api.onchange('fan_ids.fan_desc_2')
    def _calc_fd_2(self):
        """
        This method is defined to find fan description for main model.
        ---------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        # Created a for loop to iterate through the recordset since we can access only one value of recordset at a time.
        for record in self:
            # Created a sub for loop for iterating through the recordset of values fetched from different model's fn
            for rr in record.fan_ids:
                record.t_2 += rr.fan_desc_2

    @api.onchange('t_1', 't_2')
    def _calc_tf(self):
        """
        This method is used to find the total constructor fandom percentage.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            if record.t_1 != 0:
                record.t_3 = 100 * (record.t_2 / record.t_1)
            else:
                record.t_3 == 0


# Defined models for all the respective relational fields defined in the main model
class Driver(models.Model):
    _name = "formula1.driver"
    _description = "Drivers"
    _order = 'd_no'

    name = fields.Char('Driver Name', required=True, help="Enter the name of the team drivers!")
    d_no = fields.Integer('Driver Number', required=True, help="Enter the driver number!")
    salary = fields.Float('Salary', group_operator='avg')
    test_driver = fields.One2many('formula1.constructors', 'driver_id', string='Simulations Driver')


class Fans(models.Model):
    _name = "formula1.fans"
    _description = "Top Fans"

    # An additional model attr called _rec_name is added because every relation field model requires a 'name' field.
    # The value passed in this '_rec_name' will be shown when we select the respective model from the menu of main.
    _rec_name = 'fan_name'

    fan_id = fields.Integer("Top Fan's ID", help="Enter top fan's id!")
    fan_name = fields.Char("Top Fan's Name", size=64, required=True, help="Enter the Top fan's name!")

    # Defining a M2O field for the respective O2M field in main model which uses this field as inverse name.
    constr = fields.Many2one(comodel_name='formula1.constructors', string='Constructor Name', ondelete="cascade")
    fan_h = fields.Float('Fan Height')
    fan_w = fields.Float('Fan Weight')
    fan_age = fields.Float('Fan Age')

    # Defined another set of fields for calculating certain some value from entered values in these fields.
    fan_desc_1 = fields.Float('Fan Desc 1', compute='_calc_fan1')
    fan_desc_2 = fields.Float('Fan Desc 2', compute='_calc_fan2')
    perc = fields.Integer('Fandom Percentage', compute='_calc_fan3')

    # Defined the functions for their respective compute fields.
    @api.onchange('fan_h', 'fan_w', 'fan_age')
    def _calc_fan1(self):
        """
        This method defined for finding out fan_desc_1."
        ----------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            record.fan_desc_1 = record.fan_h + record.fan_w + record.fan_age

    @api.onchange('fan_h', 'fan_w', 'fan_age')
    def _calc_fan2(self):
        """
        This method is defined for finding out fan_desc_2
        ----------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            record.fan_desc_2 = record.fan_h + record.fan_w - record.fan_age

    @api.onchange('fan_desc_2', 'fan_desc_1')
    def _calc_fan3(self):
        """
        This method is defined for finding out fandom_percentage
        ----------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            if record.fan_desc_1 != 0:
                record.perc = 100 * (record.fan_desc_2 / record.fan_desc_1)
            else:
                record.perc == 0


class Circuit(models.Model):
    _name = 'formula1.circuit'
    _description = 'Circuits'
    _rec_name = 'c_name'

    c_name = fields.Char('Circuit Name', size=64, help='Enter the circuit name!')
    const_cost = fields.Integer('Construction Costs', group_operator='max')


class Part(models.Model):
    _name = 'formula1.part'
    _description = 'Parts Supplier'
    _table = 'formula1_part'
    _rec_name = 'ps_name'

    ps_id = fields.Integer('Parts Supplier ID')
    ps_name = fields.Char('Parts Supplier', size=64, help='Enter the various parts supplier for this constructor!')
