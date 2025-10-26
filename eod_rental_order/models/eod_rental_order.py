# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EODRentalOrder(models.Model):
    _name = 'eod.rental.order'
    _description = 'EasyOutDesk Rental Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'order_number'


    name = fields.Char(string='Name', required=False)
    order_number = fields.Char(string="Order Number", readonly=True, copy=False,
                               default=lambda self: self.env['ir.sequence'].next_by_code('bike.request.sequence'))
    number_plate = fields.Char(related='bike_id.number_plate',string="Bike Number Plate", readonly=True, copy=False)

    bike_id = fields.Many2one(
        'eod.bike', string="Bike", required=True, tracking=True)
    shop_id = fields.Many2one(
        'bike.shop', string="Shop", required=False)
    customer_id = fields.Many2one(
            'res.partner', string="Customer", required=True, tracking=True)

    rental_date = fields.Datetime(
        string="Rental Date",
        required=True, default=lambda self: fields.Datetime.now())

    return_date = fields.Datetime(string="Return Date",
                                  required=True, tracking=True)

    rate = fields.Float(string="Rate",tracking=True,
        compute="_compute_rate",store=True,readonly=True)

    period = fields.Selection([('day', 'Day'), ('hourly', 'Hourly')])
    spent_period = fields.Float(string="Spent Period")
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('reject', 'Rejected'),
        # ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ], string="Status", default='draft', tracking=True)

    note = fields.Text(string="Notes")
    description = fields.Html(string="Description")
    reject_reason = fields.Text(string="Reject Reason", tracking=True, readonly=True)
    rejected_by = fields.Many2one('res.users', string="Rejected By", tracking=True, readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('order_number'):
                vals['order_number'] = self.env['ir.sequence'].next_by_code('bike.request.sequence')
        records = super(EODRentalOrder, self).create(vals_list)
        return records

    @api.depends('bike_id', 'period')
    def _compute_rate(self):
        for rec in self:
            if rec.bike_id and rec.period:
                if rec.period == 'day':
                    rec.rate = rec.bike_id.day_rent
                elif rec.period == 'hourly':
                    rec.rate = rec.bike_id.hourly_rent
            else:
                rec.rate = 0.0

    # @api.onchange('bike_id', 'period')
    # def _onchange_bike_or_period(self):
    #     for rec in self:
    #         if rec.bike_id and rec.period:
    #             if rec.period == 'day':
    #                 rec.rate = rec.bike_id.day_rent
    #             elif rec.period == 'hourly':
    #                 rec.rate = rec.bike_id.hourly_rent
    #         else:
    #             rec.rate = 0.0


    @api.depends('spent_period','rate')
    def _compute_total_amount(self):
        for rec in self:
            if rec.spent_period and rec.rate:
                rec.total_amount = rec.spent_period * rec.rate
            else:
                rec.total_amount = 0.0

    def button_approval_request(self):
        for rec in self:
            rec.state = 'to_approve'

    def button_approve(self):
        for rec in self:
            rec.state = 'approved'

    def button_reject(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'bike.request.reject',
            'target': 'new',
            'context': {
                'active_id': self.id
            }
        }

    def button_cancel(self):
        for rec in self:
            rec.state = 'cancelled'
