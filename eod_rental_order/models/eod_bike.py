from odoo  import models,fields

class EODBike(models.Model):
    _name = 'eod.bike'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Eod Bike Management"


    name = fields.Char(string="Name", required=True)
    date = fields.Datetime(string="Date")
    type = fields.Selection([('fuel','Fuel'),('electric','Electric')])
    is_available = fields.Boolean(string="Available")
    state = fields.Selection([('draft','Draft'),('confirm','Confirm')])
    image = fields.Binary(string="Bike Image")

    number_plate = fields.Char(string="Number Plate", required=True)
    vin_number = fields.Char(string="VIN / Chassis Number")
    registration_date = fields.Date(string="Registration Date")
    color = fields.Char(string="Color")
    engine_capacity = fields.Integer(string="Engine CC")

    note = fields.Html(string='Notes')

    day_rent = fields.Float(string="Daily Rent")
    hourly_rent = fields.Float(string="Hourly Rent")

    # _sql_constraints = [
    #     ('number_plate_unique', 'unique(number_plate)', 'The number plate must be unique!')
    # ]

    _unique_number_plate = models.Constraint(
        'UNIQUE(number_plate)',
        'The number plate must be unique!',
    )
