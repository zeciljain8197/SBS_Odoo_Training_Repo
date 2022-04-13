from odoo import models, fields, api


class Formula1OverallReport(models.AbstractModel):
    _name = 'report.formula1.report_overall'
    _description = 'Overall Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("DOC IDS", docids)
        print("DATA", data)
        if not docids:
            docids = data['docids']
        return {
            'doc_ids': docids,
            'doc_model': self.env['formula1.constructors'],
            'data': data,
            'docs': self.env['formula1.constructors'].browse(docids),
            'zinu': 'Hello Zecil',
            'get_total_fandom': self._get_total_fandom,
            'fetch_fans': self._fetch_fans,
        }

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
