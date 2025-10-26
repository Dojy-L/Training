from reportlab.graphics.shapes import String

from odoo  import models,fields,api


class BikeRequestReject(models.TransientModel):
    _name = 'bike.request.reject'
    _description = 'Bike Request Reject Reason'

    reason = fields.Text(string="Reject Reason")
    rental_order_id = fields.Many2one('eod.rental.order', string="Rental Order")

    # @api.model
    # def default_get(self, fields_list):
    #     result = super().default_get(fields_list)
    #     result['res_id'] = self._context.get('active_id')
    #     return result

    @api.model
    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        result['rental_order_id'] = self._context.get('active_id')
        return result

    def confirm_reject(self):
        rental_order = self.env['eod.rental.order'].browse(self.env.context.get('active_id'))
        rental_order.write({
            'state': 'reject',
            'reject_reason': self.reason,
            'rejected_by': self.env.user.id,
        })
        return {'type': 'ir.actions.act_window_close'}

