# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real estate Property Offer'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection([('accepted','accepted'),('refused','refused')],string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', String="Buyer", copy=False, required=True)
    property_id = fields.Many2one('estate.property', string="Name", required=True)

    property_type_id = fields.Many2one(string="Property Type", related='property_id.property_type_id')

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_date_deadline',inverse='_inverse_date_deadline', store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        print("_compute_date_deadline")
        for rec in self:
            rec.date_deadline = fields.Date.today() + relativedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            print("_inverse_date_deadline---------------->")
            if rec.date_deadline:
                rec.validity = (rec.date_deadline - fields.Date.today()).days
            else:
                rec.validity = 0
                # rec.validity = (rec.date_deadline - fields.Date.today()).days