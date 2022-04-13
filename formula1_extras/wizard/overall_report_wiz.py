from odoo import models, fields, api


# Ex 8 Ques 19
class OverallReportWizard(models.TransientModel):
    _inherit = 'overall.report.wizard'

    entry_fees = fields.Float('EntryFees')
    c_code = fields.Char('Constructor Code', required=True)

    def html_method_wiz(self):
        report = super().html_method_wiz()
        return report

    def pdf_method_wiz(self):
        report = super().pdf_method_wiz()
        return report
