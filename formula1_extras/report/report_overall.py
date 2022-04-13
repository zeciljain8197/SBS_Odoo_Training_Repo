from odoo import models, fields, api


class Formula1OverallReport(models.AbstractModel):
    _inherit = 'report.formula1.report_overall'

    @api.model
    def _get_report_values(self, docids, data=None):
        values = super()._get_report_values(docids, data=data)
        values.update({
            'test': self.testing,
        })
        return values

    def testing(self):
        var = "Testing Variable"
        return var