from odoo import models, fields


class UpdateFanVisit(models.TransientModel):
    _name = 'update.fan.visit'
    _description = 'Update Fan Visit'

    fan_id = fields.Many2one('multiple.inheritance', 'Circuit Name')
    visited = fields.Selection(
        selection=[('yt', 'Yet to Visit'), ('vtw', 'Visiting this Weekend'), ('av', 'Already visited')],
        string='Visit Info')
    visit_review = fields.Boolean('Was Visit Satisfactory?')

    def update_fan_visit(self):
        """"
        This method is used to update fan visit info
        ------------------------------------------
        :param self: object pointer
        """
        f_vis = self.fan_id
        if not f_vis.ids:
            f_vis_ids = self._context.get('active_ids')
            f_vis_obj = self.env[self._context.get('active_model')]
            f_vis = f_vis_obj.browse(f_vis_ids)
        f_vis.write({
            'visited': self.visited,
            'visit_review': self.visit_review,
        })

