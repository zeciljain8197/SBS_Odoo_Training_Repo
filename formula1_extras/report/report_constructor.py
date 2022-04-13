from odoo import models, fields, api


#  Ex 8 Ques 18
class Formula1ConstructorReport(models.AbstractModel):
    _inherit = 'report.formula1.report_constructor'

    @api.model
    def _get_report_values(self, docids, data=None):
        values = super()._get_report_values(docids, data=data)
        values.update({
            'Nationality': 'India',
            'Age': '22',
            'time_stamp': fields.Datetime.now(),
            'get_total_fandom': self._get_total_fandom,
            'fetch_fans': self._fetch_fans,
        })
        return values

    def _get_total_fandom(self, percs):
        total = 0.0
        for perc in percs:
            total += perc.perc
        return total

    def _fetch_fans(self, fans):
        lst = []
        for fan in fans:
            lst.append(fan.fan_name)
        obj = ','.join(map(str, lst))
        return obj
