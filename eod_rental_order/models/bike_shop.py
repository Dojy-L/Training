from odoo import models, fields

class BikeShop(models.Model):
    _name = 'bike.shop'
    _description = 'Bike Rental Shop'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Shop Name', required=True, tracking=True)
    code = fields.Char(string='Shop Code', required=True, tracking=True)
    location = fields.Char(string='Location', tracking=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    manager_id = fields.Many2one('res.users', string='Shop Manager')
    is_active = fields.Boolean(string='Active', default=True)
    note = fields.Text(string='Notes')

    bike_ids = fields.Many2many('eod.bike', string='Bikes in this Shop')
