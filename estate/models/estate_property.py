# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate Properties'
    _order = 'id desc'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    description = fields.Char(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Date availability", copy=False, default=lambda self: fields.Date.today() + relativedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", default=0.0, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          string="Garden Orientation", default='north')
    state = fields.Selection([('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'),
                              ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, copy=False, default='new')
    property_type_id = fields.Many2one('estate.property.type', string="Type")
    user_id = fields.Many2one('res.users', string="Sales Person", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer Ids')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    total_area = fields.Float(compute='_compute_total_area', string="Total Area")
    best_price = fields.Float(compute='_compute_best_price', string="Best Price")

    @api.depends('total_area', 'living_area')
    def _compute_total_area(self):
        print("_compute_total_area")
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            if not rec.garden:
                rec.garden_area = 0
                rec.garden_orientation = ''
            else:
                rec.garden_orientation = 'north'


    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for rec in self:
            if rec.date_availability:
                if rec.date_availability < fields.Date.today():
                    return {
                        'warning': {
                            'title': ('Warning'),
                            'message': _('Date availability should not lower than today')
                        }
                    }

    def action_sold(self):
        for rec in self:
            if rec.state == 'canceled':
                raise UserError(_("Canceled Property Cant be Sold"))
            else:
                 rec.state = 'sold'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError(_("Sold Property Cant be Cancel"))
            else:
                rec.state = 'canceled'

    _expected_price_positive = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price must be positive.',
    )

    _selling_price_positive = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive.',
    )

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("The expected price must be positive.")

    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price and rec.expected_price:
                if rec.selling_price < 0.90 * rec.expected_price:
                    raise ValidationError(_("Selling price not lower than 90% of the expected price"))

