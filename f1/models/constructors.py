from odoo import models, fields
from datetime import datetime

cr_dt = datetime.today()


class Constructors(models.Model):
    _name = 'f1.constructors'
    _description = 'Constructors'
    _table = 'f1_constructors'
    _order = 'const_id'
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
    engine = fields.Selection(
        selection=[('mercedes', 'Mercedes'), ('redbull', 'Redbull'), ('ferrari', 'Ferrari'), ('porfields.sche', 'Porsche')],
        string='Engine supplier', help="Enter Constructor Engine supplier!")
    test_entry = fields.Char('TestEntry', size=4, default="F1")
    password = fields.Char('Password')
    email = fields.Char('Email')
    webst = fields.Char('URL')
    priority = fields.Selection([(str(ele), str(ele)) for ele in range(5)], 'Priority')
    sign_in = fields.Float('Sign In')
    sign_out = fields.Float('Sign Out')
