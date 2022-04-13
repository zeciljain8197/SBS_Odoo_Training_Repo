from odoo import models, fields, api


# Ex 8 Ques 8
class OverallReportWizard(models.TransientModel):
    _name = 'overall.report.wizard'

    driver_id = fields.Many2one('formula1.driver', 'Driver')
    const_id = fields.Many2one('formula1.constructors', 'Constructor')
    fav_circuit = fields.Char('Favourite Circuit')
    date = fields.Datetime('Date of Visit')
    wins = fields.Integer('No. of Wins')

    def html_method_wiz(self):
        const_obj = self.env['formula1.constructors']
        constructors = const_obj.search([('driver_id', '=', self.driver_id.id)])
        constructor_report = self.env.ref('formula1.overall_report_html')
        print("Test--------------------->", self.read()[0])
        data = {
            'model': 'overall.report.wizard',
            'form': self.read()[0],
            'docids': constructors.ids,
        }
        print("_______________________", constructors.ids, data)
        return constructor_report.report_action(constructors.ids, data=data, config=True)

    def pdf_method_wiz(self):
        const_obj = self.env['formula1.constructors']
        constructors = const_obj.search([('driver_id', '=', self.driver_id.id)])
        constructor_report = self.env.ref('formula1.overall_report_pdf')
        data = {
            'model': 'overall.report.wizard',
            'form': self.read()[0],
            'docids': constructors.ids,
        }
        return constructor_report.report_action(constructors.ids, data=data, config=True)
