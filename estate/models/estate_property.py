# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real estate Properties'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    description = fields.Char(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Date availability")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden", default=True)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          string="Garden Orientation")
    state = fields.Selection([('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'),
                              ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, copy=False, default='new')

    property_type_id = fields.Many2one('estate.property.type', string="Type")
    user_id = fields.Many2one('res.users', String="Sales Person", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', String="Buyer", copy=False)

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
        print("OOOOOOOOOOO")
        for rec in self:
            if not rec.garden:
                rec.garden_area = 0
                rec.garden_orientation = ''

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for rec in self:
            if rec.date_availability:
                if rec.date_availability < fields.Date.today():
                    return {'warning': {
                        'title': _('Warning'),
                        'message': _('The availability date cannot be set before today.')
                    }}
