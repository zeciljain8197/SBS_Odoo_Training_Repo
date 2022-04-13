from odoo import models, fields


# Ex 8 Ques 4
class ConstructorReportWizardSimple(models.TransientModel):
    _name = 'constructor.report.wizard.simple'

    driver_id = fields.Many2one('formula1.driver', 'Driver Name')

    def html_method_simple(self):
        const_obj = self.env['formula1.constructors']
        constructors = const_obj.search([('driver_id', '=', self.driver_id.id)])
        constructor_report = self.env.ref('formula1.constructor_report_html')
        return constructor_report.report_action(constructors.ids, data=None, config=True)

    def pdf_method_simple(self):
        const_obj = self.env['formula1.constructors']
        constructors = const_obj.search([('driver_id', '=', self.driver_id.id)])
        constructor_report = self.env.ref('formula1.constructor_report_pdf')
        return constructor_report.report_action(constructors.ids, data=None, config=True)


class ConstructorReportWizard(models.TransientModel):
    _name = 'constructor.report.wizard'

    driver_id = fields.Many2one('formula1.driver', 'Driver')

    def html_method(self):
        const_obj = self.env['formula1.constructors']
        constructors = const_obj.search([('driver_id', '=', self.driver_id.id)])
        constructor_report = self.env.ref('formula1.constructor_report_html')
        data = {
            'form': self.read()[0],
            'docids': constructors.ids
        }
        print("_______________________", constructors.ids, data)
        return constructor_report.report_action(constructors.ids, data=data, config=True)

    def pdf_method(self):
        const_obj = self.env['formula1.constructors']
        constructors = const_obj.search([('driver_id', '=', self.driver_id.id)])
        constructor_report = self.env.ref('formula1.constructor_report_pdf')
        data = {
            'form': self.read()[0],
            'docids': constructors.ids
        }
        return constructor_report.report_action(constructors.ids, data=data, config=True)

