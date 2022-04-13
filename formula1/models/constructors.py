from odoo import models, fields, api, exceptions, tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

# Importing the packages from odoo module

# Creating a date value for using in the models
cr_dt = datetime.today()


# Creating a model of name:Constructors by creating its class
class Constructors(models.Model):
    # Defining model attributes
    _name = 'formula1.constructors'
    _description = 'Constructors'
    _table = 'formula1_constructors'
    _order = 'sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # Defining parent_name and parent_path for hierarchy of this model
    _parent_name = 'parent_id'
    _parent_store = True

    # Ques 19-21 and 26
    _sql_constraints = [
        ('unique_wbst', 'unique(wbst)', 'The constructor must have unique website!'),
        ('unique_name', 'unique(const_id, name)', 'The Constructor name must be unique along with its ID!'),
        ('check_entry_fees', 'check(entry_fees>2000000)', 'The entry fees must be greater than a million dollars!'),
    ]

    # Ques 22
    @api.constrains('c_code')
    def check_c_code(self):
        """
        Check age based on the dob
        --------------------------
        :param self: object pointer
        """
        for const in self:
            if len(const.c_code) != 3:
                raise ValidationError("The Constructor Code must be of length 3!")
            if const.const_id > 10:
                raise ValidationError("Please enter a value less than 10!")

    # Defining various fields of the model
    const_id = fields.Integer('Number', default=False, help="Enter Constructor Number!")
    name = fields.Char('Constructor Name', required=True, size=64, trim=True, help="Enter Constructor Name!")
    c_code = fields.Char('Constructor Code', required=True)
    entry_fees = fields.Float('EntryFees', digits=(16, 3), help="Enter Constructor entry-fees!")
    active = fields.Boolean('Active', default=True, help="Enter Constructor active status!")
    const_notes = fields.Text('Constructor Notes', help="Enter any notes regarding the constructor!")
    driver1_notes = fields.Text('Driver1 Notes', help="Enter any notes regarding the drivers!")
    driver2_notes = fields.Text('Driver2 Notes', help="Enter any notes regarding the drivers!")
    html = fields.Html('Constructor Fanpage', help="Enter html!")
    st_date = fields.Datetime('Join Date', help="Enter Constructor start date!")
    nxt_date = fields.Date('Next Fanfest', default=cr_dt, help="Enter Constructor's next fanfest date'!")
    test_str = fields.Datetime('Team testing session start')
    test_end = fields.Datetime('Team testing session end')
    podiums = fields.Char('Podiums')
    wins = fields.Integer('No. of Wins')
    winner = fields.Boolean('Previous Wins')
    win_notes = fields.Text('Past race wins')
    # Defining a selection field for drop down menu of various values to choose from! It will have a list of tuples
    engine = fields.Selection(
        selection=[('mercedes', 'Mercedes'), ('redbull', 'Redbull'), ('ferrari', 'Ferrari'),
                   ('renault', 'Renault')],
        string='Engine supplier', tracking=True, help="Enter Constructor Engine supplier!")
    # Ex 6 Ques 16 above
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
    # 'Parts Supplier', domain=[('ps_name', 'ilike', '%Re')])

    # Defining a M2O field for currency having comodel-res.currency, fetching all available currencies from that model
    currency_id = fields.Many2one('res.currency', 'currency')

    # Defining Monetary field which is going to be used to select the currency to be selected!
    val = fields.Monetary(currency_field='currency_id', string='Valuation')

    # Defining a Reference field which works as a combination of Selection and M2O fields
    extra_info = fields.Reference(
        selection=[("formula1.driver", "Drivers"), ("formula1.fans", "Fans"), ("formula1.circuit", "Circuits")])

    # Defining fields for uploading Documents/Images on the server
    docu = fields.Binary('Constructor Info', attachment=True, help='Enter the constructor logo here!')
    img = fields.Image('Constructor Logo', default='image_128')

    # Defining a field for preserving the file name of the uploaded file
    file_name = fields.Char()

    # Defining fields where we will compute certain values automatically using compute attr and passing fn in them.
    t_1 = fields.Float('Fan Description 1', compute='_calc_fd_1')
    t_2 = fields.Float('Fan Description 2', compute='_calc_fd_2')
    t_3 = fields.Float('Total Fandom %', compute='_calc_tf')
    state = fields.Selection(
        selection=[('s1', 'Established Team'), ('s2', 'Title Contender'), ('s3', 'Sister Team'), ('s4', 'Underdog'),
                   ('s5', 'New Entrant')], default='s1', string='States')

    # Defining a field for giving sequencing feature to the tree view
    sequence = fields.Integer('Sequence')

    # Defining parent_id which will be a M2O field for giving hierarchy of the main model
    parent_id = fields.Many2one('formula1.constructors', string='Supplier Team',
                                domain=[('name', '!=', name)])

    # Defining child_ids(O2M) for the respective parent_id(M2O) to create its child fields
    child_ids = fields.One2many('formula1.constructors', 'parent_id', string='Consumer Teams')

    # Defining a field parent_path which will be used to store the hierarchy of each field in the DB
    parent_path = fields.Char('parent_path')

    fan_count = fields.Integer('Fan count', compute='fan_ct')

    current_user = fields.Many2one('res.users', string='Current user')

    clr = fields.Integer('Color Index')

    team_count = fields.Integer('Academy Team count', compute='academy_ct')

    # Ex 7 Ques 8
    def academy_ct(self):
        """
        This method is used to count related academies of the current record
        @param self: object pointer/ Recordset
        """
        rec = self.env['formula1.extras.teams']
        for team in self:
            team.team_count = rec.search_count([('main_team', '=', team.id)])
        action = self.env.ref('formula1_extras.action_teams_wiz').read()[0]
        return action

    # Ques 24
    # @api.model_create_multi
    @api.model
    def create(self, values):
        """
        Overridden create() method to add sequence
        ------------------------------------------
        :param self: object pointer
        :param vals_list: List of dictionary containing fields and values
        :return: recordset of the newly created record(s)
        """
        # seq = self.env.ref('formula1.constructors_const_id_seq')
        # for vals in vals_list:
        #     vals['name'] = seq.next_by_id()
        # return super().create(vals_list)
        if 'img' in values:
            image = tools.ImageProcess(values['img'])
            resize_image = image.resize(300, 300)
            resize_image_b64 = resize_image.image_base64()
            values['img'] = resize_image_b64
        obj = super().create(values)
        return obj

    def write(self, vals):
        if 'img' in vals:
            image = tools.ImageProcess(vals['img'])
            resize_image = image.resize(300, 300)
            resize_image_b64 = resize_image.image_base64()
            vals['img'] = resize_image_b64
        obj = super().write(vals)
        return obj

    # Ques17
    @api.onchange('driver_id')
    def onchange_part(self):
        """
        This method sets a domain on another field based on the value selected.
        -----------------------------------------------------------------------
        :param self: object pointer
        :return: A dictionary containing a domain
        """
        dom = []
        if self.driver_id:
            dom = [('driver_id', '=', self.driver_id.id)]
        res = {
            'domain': {
                'fav_ids': dom
            }
        }
        return res

    def button_for_env(self):
        """
        This method is defined to compute results of environment methods.
        ---------------------------------------------------------------
        @param self: object pointer / Recordset
        """

        res_lang = self.env.lang
        print(res_lang)
        res_comp = self.env.company.name
        print(res_comp)
        res_user = self.env.user.name
        print(res_user)
        res_cont = self.env.context
        print(res_cont)
        res_ref = self.env.ref('formula1.view_constructors_form')
        print(res_ref)
        res1 = self.env['formula1.driver'].search([])
        res_meta = res1.get_metadata()
        print(res_meta)
        res_filter = res1.filtered(lambda z: z.d_no <= 20)
        print(res_filter)
        res_filter1 = res1.filtered(lambda e: e.salary == False)
        print(res_filter1)
        res_concat = res1.mapped(lambda c: c.name + '-' + str(c.d_no))
        print(res_concat)
        res_part = res1.mapped('salary')
        print("Values of recordset: ", res_part)
        res_desc = res1.sorted(key='d_no', reverse=True)
        print(res_desc)
        res2 = self.env['formula1.constructors'].search([])
        print(res2)
        res2_sub1 = res2.filtered(lambda res1: res1.engine == 'redbull')
        print(res2_sub1)
        res2_sub2 = res2.filtered(lambda res2: res2.engine == 'mercedes')
        print(res2_sub2)
        res2_sub1_sub = res2_sub1 > res2_sub2
        print(res2_sub1_sub)
        res2_sub2_sub = res2_sub2 > res2_sub1
        print(res2_sub2_sub)
        res2_sub_1 = res2 > res2_sub1
        print(res2_sub_1)
        res2_sub_2 = res2 > res2_sub2
        print(res2_sub_2)
        res_union = res2_sub1 | res2_sub2
        print(res_union)
        res_inter = res2 & res2_sub2
        print(res_inter)
        res_diff = res2 - res2_sub2
        print(res_diff)
        res_search = self.env['formula1.fans'].search([('constr', '=', 7)], offset=1, limit=4, order='fan_name')
        print("Result for fetching records: ", res_search)
        res_fetch = self.search([('entry_fees', '<=', 10)], count=True)
        res_fetch_1 = self.search_count([('entry_fees', '<=', 10)])
        print("Result with search:", res_fetch, "Result without search:", res_fetch_1)
        res_count = self.search_count([('entry_fees', '>', 0)])
        print("Result for counting: ", res_count)
        res_fetch = self.search_read([('entry_fees', '<=', 10)])
        print("Result without using search or read:", res_fetch)
        res_read = self.search_read(fields={'const_id', 'name', 'engine'}, order='name')
        print("Result without using domain:", res_read)
        res_cuser = self.env['res.users'].search([('login', '=', 'admin')])
        # res_cuser = self._uid
        print("Current user", res_cuser)
        res_uid = self.create_uid
        print("Record Creator: ", res_uid)

    # Defining a decorator for all the functions to reflect any changes made to their values on runtime itself
    @api.onchange('fan_ids.fan_desc_1')
    def _calc_fd_1(self):
        """
        This method is defined to find fan description for main model.
        ---------------------------------------------------------------
        @param self: object pointer / Recordset
        """

        self.t_1 = 0
        for record in self:
            for r_sub in record.fan_ids:
                record.t_1 += r_sub.fan_desc_1

    # The values which are passed in the decorator are the values that the fn depends on.
    # Means when those values are changed, the main value of the fn will also get changes accordingly.
    @api.onchange('fan_ids.fan_desc_2')
    def _calc_fd_2(self):
        """
        This method is defined to find fan description for main model.
        ---------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        self.t_2 = 0
        # Created a for loop to iterate through the recordset since we can access only one value of recordset at a time.
        for record in self:
            # Created a sub for loop for iterating through the recordset of values fetched from different model's fn
            for r_sub in record.fan_ids:
                record.t_2 += r_sub.fan_desc_2

    @api.onchange('t_1', 't_2')
    def _calc_tf(self):
        """
        This method is used to find the total constructor fandom percentage.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        self.t_3 = 0
        for record in self:
            if record.t_1 != 0:
                record.t_3 = 100 * (record.t_2 / record.t_1)
            else:
                record.t_3 = 0

    def new_record(self):
        """
        This method is used to create new record.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        driver = self.env['formula1.driver']
        vals_list = []
        vals = {
            'name': 'George Russell',
            'd_no': '63',
            'salary': '70000000'
        }
        vals_list.append(vals)
        driver_new = driver.create(vals_list)

    def new_one2many(self):
        """
        This method is used to create new record in one2many field.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        fans_new = self.write({'fan_ids': [(0, 0, {'fan_id': '8',
                                                   'fan_name': 'Vishwa Parker',
                                                   'constr': 8,
                                                   'fan_h': 5.9,
                                                   'fan_w': 76.00,
                                                   'fan_age': 22})]})

    def update_rec(self):
        """
        This method is used to update the existing records.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        rec_updt = self.env['formula1.circuit']
        rec_updt_br = rec_updt.browse(2)
        up_rec = {
            'const_cost': 1850000000
        }
        updt = rec_updt_br.write(up_rec)

    def unlink_rec(self):
        """
        This method is used to remove one or multiple records from gui but not from database.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        res = self.write({'fan_ids': [(3, 9)]})

    def unlink_all(self):
        """
        This method is used to unlink all records of the model.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        res = self.write({'fan_ids': [(5, 0, 0)]})

    def link_ids(self):
        """
        This method is used to link few records of the model.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        res = self.write({'fav_ids': [(6, 0, [1, 2])]})

    def fan_ct(self):
        """
        This method is used to count related records of the current record
        @param self: object pointer/ Recordset
        """
        rec = self.env['formula1.fans']
        for fan in self:
            fan.fan_count = rec.search_count([('constr', '=', fan.id)])
        # view_id = self.env.ref('view_fans_tree').id
        # return {
        #     'name': 'Tree view of fans',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'tree',
        #     'res_model': 'formula1.fans',
        #     'view_id': view_id,
        #     'context': {'search_default_fan_id': self.id, 'default_fan_id': self.id}
        #
        # }

    def cur_user(self):
        """
        This method is used to pass the name of current logged-in user automatically to our M2O field.
        ---------------------------------------------------------------------
        @param self: object pointer / Recordset
        """
        self.current_user = self.env.user

    # # Ques1 and 3
    # @api.model_create_multi
    # def create(self, vals_list):
    #     """
    #     Overridden create() method to set the code from the name
    #     --------------------------------------------------------
    #     :param self: object / blank recordset
    #     :param vals_list: A list of dictionary containing fields and values, used to create records
    #     :return: A recordset of newly created records
    #     """
    #     d_obj = self.env['formula1.driver']
    #     vals_lst = [{
    #         'd_no': 10,
    #         'name': 'Test Driver',
    #         'salary': 1000000,
    #         'd_code': 'DRI'
    #     }]
    #     d_obj.create(vals_lst)
    #     res = super().create(vals_list)
    #     print('Create method override', res)
    #     rec = d_obj.browse(3)
    #     rec.write({
    #         'd_code': 'LEC'
    #     })
    #     return res

    # Ques25
    def create_sequence(self):
        """
        Method to set the sequence on any field
        --------------------------------------------------------
        :param self:object /recordset
        """
        for const in self:
            const.email = self.env['ir.sequence'].next_by_code('formula1.constructors')

        # seq = self.env.ref('formula1.constructors_const_id_seq')
        # res['name'] = seq.next_by_id()

    # Ques 13-14
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """
        Overridden fields_view_get() method to set the attributes of views
        -------------------------------------------------------------------
        :param self: object / Recordset
        """
        res = super(Constructors, self).fields_view_get(view_id, view_type, toolbar=toolbar,
                                                        submenu=False)
        print('View type----->', view_type)
        print(res)
        if view_type == 'form':
            print('---------------Sortable form--------------', res.get('fields').get('engine').get('sortable'))
            change = res.get('fields').get('state').update({'sortable': False})
        elif view_type == 'tree':
            print('---------------Sortable tree--------------', res.get('fields').get('engine').get('sortable'))
            change = res.get('fields').get('state').update({'sortable': False})
        elif view_type == 'search':
            print('---------------Sortable search--------------', res.get('fields').get('engine').get('sortable'))
            change = res.get('fields').get('engine').update({'sortable': False})
        return res


# Defined models for all the respective relational fields defined in the main model
class Driver(models.Model):
    _name = "formula1.driver"
    _description = "Drivers"
    _order = 'd_no'

    name = fields.Char('Driver Name', required=True, help="Enter the name of the team drivers!", copy=False)
    d_no = fields.Integer('Driver Number', required=True, help="Enter the driver number!")
    fan_id = fields.Many2one('formula1.fans', "Fan Name")
    salary = fields.Float('Salary')
    # group_operator = 'avg'
    test_driver = fields.One2many('formula1.constructors', 'driver_id', string='Main Driver For')
    d_code = fields.Char('Driver Code', copy=False)
    d_state = fields.Selection(
        selection=[('d1', 'Legendary'), ('d2', 'Veteran'), ('d3', 'Title Competitor'), ('d4', 'Experienced'),
                   ('d5', 'Rookie')], string='Experience', copy=False)
    d_nation = fields.Many2one('res.country', 'Nationality')
    d_wins = fields.Integer('No of Wins')
    d_podiums = fields.Integer('No of Podiums')
    d_o_b = fields.Date('Date of Birth')
    age = fields.Integer('Driver Age')
    img = fields.Image('Driver Image')
    clr = fields.Integer('Color Index')

    # Ex 7 Ques 7
    def update_driver_wins_2(self):
        """
        This method is used to Update driver wins by directly calling the action
        -----------------------------------------------------------------------
        :param self: object pointer
        """
        action = self.env.ref('formula1.action_update_driver_wins').read()[0]
        return action

    # # Ques2
    @api.model_create_multi
    def create(self, vals_list):
        """
        Overridden create() method to set the code from the name
        --------------------------------------------------------
        :param self: object / blank recordset
        :param vals_list: A list of dictionary containing fields and values, used to create records
        :return: A recordset of newly created records
        """
        # for vals in values:
        #     if not vals.get('d_code', False):
        #         vals['d_code'] = vals.get('name').split()[1][:3].upper()
        # res = super().create(values)
        # print('Create method override', res)
        if 'img' in vals_list:
            image = tools.ImageProcess(vals_list['img'])
            resize_image = image.resize(300, 300)
            resize_image_b64 = resize_image.image_base64()
            vals_list['img'] = resize_image_b64
        obj = super().create(vals_list)
        return obj

    def write(self, vals):
        if 'img' in vals:
            image = tools.ImageProcess(vals['img'])
            resize_image = image.resize(300, 300)
            resize_image_b64 = resize_image.image_base64()
            vals['img'] = resize_image_b64
        obj = super().write(vals)
        return obj

    # Ques4
    # def write(self, vals):
    #     """
    #     Overridden write() method to change the salary.
    #     ------------------------------------------------------------
    #     :param self: object pointer
    #     :param vals: a dictionary containing fields and values
    #     :return: True
    #     """
    #     if vals.get('d_code', False):
    #         vals['d_no'] = vals.d_no + 1
    #     res = super().write(vals)
    #     print('Write method override', res)
    #     return res

    # Ques5-7
    def copy(self, default=None):
        """
        Overridden copy() method to avoid duplicate names
        -------------------------------------------------
        :param self: object pointer
        :param default: a dictionary to update fields before creation
        :return: A recordset of newly created record
        """
        default = {
            'name': self.name + ' (Reserve Driver)',
            'd_code': self.d_code + ' RES',
            'd_state': 'd5'
        }
        res = super().copy(default=default)
        print('Copy method override', res)
        return res

    # Ques8
    def unlink(self):
        """
        Overridden unlink() method to avoid deletion if it's linked to some constructor
        ---------------------------------------------------------------------------
        :param self: object pointer / recordset containing records
        :return: True
        """
        d_obj = self.env['formula1.constructors']
        driver = d_obj.search([('driver_id', '=', self.id)])
        if driver:
            raise ValidationError("This driver is a test driver already!!")
        return super().unlink()

    # Ques9
    def name_get(self):
        """
        Overridden name_get method to display name and d_no
        ----------------------------------------------------
        :param self: object pointer
        :return: A list of tuple containing id and name / string to be displayed
        """
        d_lst = []
        for driver in self:
            driver_str = ""
            if driver.d_no:
                driver_str += "[" + str(driver.d_no) + "]"
            driver_str += driver.name
            d_lst.append((driver.id, driver_str))
        return d_lst

    # Ques10
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        Overridden name_search method to search based on name and d_no
        --------------------------------------------------------------
        :param self: object pointer
        :param name: the string typed in for searching the name
        :param args: the domain passed on the field
        :param operator: default is ilike so can search the matching string
        :param limit: max no of records
        :return: A list of tuple containing id and name(same as name_get)
        """
        nsrch = ['|', ('d_no', operator, name), ('name', operator, name)]
        if args:
            nsrch += args
        drivers = self.search(nsrch, limit=limit)
        return drivers.name_get()

    # Ques12, 23, 24
    # @api.model
    # def default_get(self, fields_list):
    #     """
    #     Overridden default_get method to update the default values
    #     ----------------------------------------------------------
    #     :param self: object pointer
    #     :param fields_list: List of all fields passed to get the default value
    #     :return: A dictionary containing fields and their default values
    #     """
    #     print("FIELDS", fields_list)
    #     res = super().default_get(fields_list)
    #     if 'salary' in res:
    #         del res['salary']
    #     res['salary'] = 10000000
    #     print("RES", res)
    #     # seq_obj = self.env['ir.sequence']
    #     # my_seq = seq_obj.next_by_code('formula1.constructors')
    #     # res['d_no'] = my_seq
    #     seq = self.env.ref('formula1.constructors_const_id_seq')
    #     res['name'] = seq.next_by_id()
    #     return res

    # Ques15
    @api.onchange('d_state')
    def onchange_state(self):
        """
        Onchange method to set salary based on driver experience
        -------------------------------------------
        :param self: object pointer
        """
        res = {}
        for driver in self:
            if driver.d_state == 'd1' or driver.d_state == 'd2':
                driver.salary = 25000000.0
            elif driver.d_state == 'd3' or driver.d_state == 'd4':
                driver.salary = 12000000.0
            elif driver.d_state == 'd5':
                driver.salary = 4500000.0
            else:
                driver.salary = 0.0
                return {
                    'warning': {
                        'title': 'Warning!',
                        'message': 'Driver has invalid experience!'
                    }
                }
            print('onchange working....')

    # Ques 16 and 18
    # @api.onchange('salary', 'test_driver')
    # def onchange_multiple(self):
    #     """
    #     Onchange method to set salary based on driver experience
    #     -------------------------------------------
    #     :param self: object pointer
    #     """
    #     res = {}
    #     for driver in self:
    #         if driver.salary >= 50000000 and driver.test_driver:
    #             driver.d_state = 'd5'
    #         elif driver.salary >= 25000000 and driver.test_driver:
    #             driver.d_state = 'd4'
    #         elif driver.salary >= 15000000 and driver.test_driver:
    #             driver.d_state = 'd3'
    #         elif driver.salary >= 7500000 and driver.test_driver:
    #             driver.d_state = 'd4'
    #         elif driver.salary >= 2500000:
    #             driver.d_state = 'd5'
    #         else:
    #             return {
    #                 'warning': {
    #                     'title': 'Warning!',
    #                     'message': 'Driver has no salary or Experience!'
    #                 }
    #             }

    # Ques11
    @api.model
    def name_create(self, name):
        """
        Overridden name_create method to add d_code to drivers
        --------------------------------------------------------------------
        :param self: object pointer
        :param name: The name used to create the record of driver
        :return: A tuple containing ID and name of the newly created activity record
        """
        vals_lst = [{
            'name': name,
            'd_code': name.split()[1][:3].upper()
        }]
        act = self.create(vals_lst)
        return act.name_get()[0]


class Fans(models.Model):
    _name = "formula1.fans"
    _description = "Top Fans"

    # An additional model attr called _rec_name is added because every relation field model requires a 'name' field.
    # The value passed in this '_rec_name' will be shown when we select the respective model from the menu of main.
    _rec_name = 'fan_name'

    fan_id = fields.Integer("Top Fan's ID", help="Enter top fan's id!")
    fan_name = fields.Char("Top Fan's Name", size=64, required=True, help="Enter the Top fan's name!")

    # Defining a M2O field for the respective O2M field in main model which uses this field as inverse name.
    constr = fields.Many2one(comodel_name='formula1.constructors', string='Constructor Name', ondelete="set null")
    d_id = fields.Many2one('formula1.driver', 'Driver Name')
    # domain=[('name', 'like', '%ed%')])
    fan_h = fields.Float('Fan Height')
    fan_w = fields.Float('Fan Weight')
    fan_age = fields.Float('Fan Age')

    # Defined another set of fields for calculating certain some value from entered values in these fields.
    fan_desc_1 = fields.Float('Fan Desc 1', compute='_calc_fan1', store=True)
    fan_desc_2 = fields.Float('Fan Desc 2', compute='_calc_fan2', store=True)
    perc = fields.Integer('Fandom Percentage', compute='_calc_fan3', store=True)

    # Defined the functions for their respective compute fields.
    @api.depends('fan_h', 'fan_w', 'fan_age')
    def _calc_fan1(self):
        """
        This method defined for finding out fan_desc_1."
        ----------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            record.fan_desc_1 = record.fan_h + record.fan_w + record.fan_age

    @api.depends('fan_h', 'fan_w', 'fan_age')
    def _calc_fan2(self):
        """
        This method is defined for finding out fan_desc_2
        ----------------------------------------------------
        @param self: object pointer / Recordset
        """
        for record in self:
            record.fan_desc_2 = record.fan_h + record.fan_w - record.fan_age

    @api.depends('fan_desc_2', 'fan_desc_1')
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
    driver_id = fields.Many2one('formula1.driver', 'Most Wins By Driver')
    img = fields.Image('Circuit Image')
    clr = fields.Integer('Color Index')

    @api.model
    def create(self, values):
        if 'img' in values:
            image = tools.ImageProcess(values['img'])
            resize_image = image.resize(300, 300)
            resize_image_b64 = resize_image.image_base64()
            values['img'] = resize_image_b64
        obj = super().create(values)
        return obj

    def write(self, vals):
        if 'img' in vals:
            image = tools.ImageProcess(vals['img'])
            resize_image = image.resize(300, 300)
            resize_image_b64 = resize_image.image_base64()
            vals['img'] = resize_image_b64
        obj = super().write(vals)
        return obj


class Part(models.Model):
    _name = 'formula1.part'
    _description = 'Parts Supplier'
    _table = 'formula1_part'
    _rec_name = 'ps_name'

    ps_id = fields.Integer('Parts Supplier ID')
    ps_name = fields.Char('Parts Supplier', size=64, help='Enter the various parts supplier for this constructor!')
