from odoo import models, fields, api


class Formula1ConstructorReport(models.AbstractModel):
    _name = 'report.formula1.report_constructor'
    _description = 'Constructor Report'

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
            'time_stamp': fields.Datetime.now(),
            'get_total_fan_desc_1': self._get_total_desc_1,
            'get_total_fan_desc_2': self._get_total_desc_2
        }

    def _get_total_desc_1(self, descs):
        total = 0.0
        for desc in descs:
            total += desc.fan_desc_1
        return total

    def _get_total_desc_2(self, descs):
        total = 0.0
        for desc in descs:
            total += desc.fan_desc_2
        return total
