from odoo import models, fields
import xlsxwriter
import base64
import io


# Ex 9 to 20
class ConstructorXLSReport(models.TransientModel):
    _inherit = 'constructor.xls.report.wiz'

    def print_xls_report(self):
        """
        This method will prepare a xls report of the constructor
        -----------------------------------------------------
        @param: self: object pointer
        :return: An XLS report
        """
        a_obj = self.env['ir.attachment']
        fans = self.env['formula1.fans']
        consts = self.env['formula1.constructors']
        # dom = []
        if self.type == 'driver':
            if self.driver_id:
                dom = [('driver_id', '=', self.driver_id.id)]
        elif self.type == 'fan' and self.fan_ids:
            consts = self.fan_ids.constr
        if not consts.ids:
            consts = consts.search(dom)

        wb = xlsxwriter.Workbook('/tmp/constructor_report.xlsx')
        cell_format = wb.add_format(
            {'bold': True, 'center_across': True, 'font_color': 'blue', 'text_wrap': True})
        font_format = wb.add_format({'center_across': True, 'text_wrap': True})
        for const in consts:
            sheet = wb.add_worksheet(const.name)
            image_width = 140.0
            image_height = 182.0
            cell_width = 64.0
            cell_height = 120.0
            x_scale = cell_width / image_width
            y_scale = cell_height / image_height
            sheet.merge_range(0, 2, 0, 7, 'Constructor Report', cell_format)
            buf_image = io.BytesIO(base64.b64decode(const.img))
            sheet.insert_image('G3', "constr.png", {'image_data': buf_image, 'x_scale': x_scale, 'y_scale': y_scale})
            sheet.write(2, 0, 'Name', cell_format)
            sheet.write(2, 1, const.name, font_format)
            sheet.write(3, 0, 'Driver', cell_format)
            sheet.write(3, 1, const.driver_id.name, font_format)
            sheet.write(3, 3, 'Engine', cell_format)
            sheet.write(3, 4, const.engine, font_format)
            sheet.write(4, 0, 'Constructor Valuation', cell_format)
            sheet.write(4, 1, const.val, font_format)
            sheet.write(5, 0, "Constructor Wins", cell_format)
            sheet.write(5, 1, const.wins, font_format)
            sheet.merge_range(6, 2, 6, 4, 'Fandom', cell_format)
            sheet.write(8, 0, 'Fan number', cell_format)
            sheet.write(8, 1, 'Fan Name', cell_format)
            sheet.write(8, 2, 'Constructor', cell_format)
            sheet.write(8, 3, 'Height', cell_format)
            sheet.write(8, 4, 'Weight', cell_format)
            sheet.write(8, 5, 'Age', cell_format)
            sheet.write(8, 6, 'Fan Desc 1', cell_format)
            sheet.write(8, 7, 'Fan Desc 2', cell_format)
            sheet.write(8, 8, 'Fandom %', cell_format)
            row = 9
            total_1 = 0.0
            total_2 = 0.0
            total_horizontal = 0.0
            chart = wb.add_chart({'type': 'column'})
            for fan in const.fan_ids:
                sheet.write(row, 0, fan.fan_id, font_format)
                sheet.write(row, 1, fan.fan_name, font_format)
                sheet.write(row, 2, fan.constr.name, font_format)
                sheet.write(row, 3, fan.fan_h, font_format)
                sheet.write(row, 4, fan.fan_w, font_format)
                sheet.write(row, 5, fan.fan_age, font_format)
                sheet.write(row, 6, fan.fan_desc_1, font_format)
                total_1 += fan.fan_desc_1
                sheet.write(row, 7, fan.fan_desc_2, font_format)
                total_2 += fan.fan_desc_2
                total_horizontal = fan.fan_h + fan.fan_w + fan.fan_age + fan.fan_desc_1 + fan.fan_desc_2
                sheet.write(row, 8, fan.perc, font_format)
                sheet.write(row, 9, total_horizontal, cell_format)
                chart.add_series({
                    'name': [const.name, row, 1],
                    'categories': [const.name, row - 1, 3, row - 1, 5],
                    'values': [const.name, row, 3, row, 5],
                })
                chart.set_title({'name': 'Fan Attributes'})
                chart.set_table()
                row += 1
            sheet.insert_chart('K1', chart)
            sheet.write(row - 2, 9, "Horizontal Total", cell_format)
            sheet.write(row, 0, "Vertical Total", cell_format)
            sheet.write(row, 6, total_1, cell_format)
            sheet.write(row, 7, total_2, cell_format)
        wb.close()

        # Ex 8 Ques 15
        f1 = open('/tmp/constructor_report.xlsx', 'rb')
        xls_data = f1.read()
        encoded = base64.b64encode(xls_data)
        doc = a_obj.create({'name': '%s.xlsx' % ('Constructor Report'),
                            'datas': encoded,
                            'res_model': 'constructor.xls.report.wiz',
                            'store_fname': '%s.xlsx' % ('Constructor Report'),
                            })
        return {'type': 'ir.actions.act_url',
                'url': 'web/content/%s?download=true' % (doc.id),
                'target': 'current'
                }
