from odoo  import models,fields

class EODBike(models.Model):
    _name = 'eod.bike'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Eod Bike Management"


    name = fields.Char(string="Name", required=True)
    date = fields.Datetime(string="Date")
    type = fields.Selection([('fuel','Fuel'),('electric','Electric')])
    is_available = fields.Boolean(string="Available", default=True)
    # state = fields.Selection([('draft','Draft'),('confirm','Confirm')])
    image = fields.Binary(string="Bike Image")

    number_plate = fields.Char(string="Number Plate", required=True)
    vin_number = fields.Char(string="VIN / Chassis Number")
    registration_date = fields.Date(string="Registration Date")
    color = fields.Char(string="Color")
    engine_capacity = fields.Integer(string="Engine CC")

    note = fields.Html(string='Notes')

    day_rent = fields.Float(string="Daily Rent")
    hourly_rent = fields.Float(string="Hourly Rent")

    rental_order_ids = fields.One2many(
        'eod.rental.order', 'bike_id', string="Rental Orders"
    )
    order_count = fields.Integer(compute='_computer_order_count')

    # _sql_constraints = [
    #     ('number_plate_unique', 'unique(number_plate)', 'The number plate must be unique!')
    # ]

    _unique_number_plate = models.Constraint(
        'UNIQUE(number_plate)',
        'The number plate must be unique!',
    )

    def _computer_order_count(self):
        for rec in self:
            rec.order_count = len(rec.rental_order_ids)

    def action_open_rental_orders(self):
        print("action_open_rental_orders")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rental Orders',
            'res_model': 'eod.rental.order',
            'view_mode': 'list,form',
            'domain': [('bike_id', '=', self.id)],
            'context': {'default_bike_id': self.id},
        }


