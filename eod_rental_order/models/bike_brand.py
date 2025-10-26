from odoo  import models,fields

class BikeBrand(models.Model):
    _name = 'bike.brand'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Bike Brands"


    name = fields.Char(string="Name", required=True)