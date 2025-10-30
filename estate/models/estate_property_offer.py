# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection([('accepted','accepted'),('refused','refused')],string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', String="Buyer", copy=False, required=True)
    property_id = fields.Many2one('estate.property', string="Name", required=True)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type", related='property_id.property_type_id', store=True)

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline',store=True)


    @api.depends('validity')
    def _compute_date_deadline(self):
        print("_compute_date_deadline")
        for rec in self:
            rec.date_deadline = fields.Date.today() + relativedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - fields.Date.today()).days

    def action_accept(self):
        print("action_accept")
        if 'accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Only one offer can accept"))
        else:
            for rec in self:
                rec.status = 'accepted'
                rec.property_id.partner_id = self.env.user.partner_id
                rec.property_id.selling_price = rec.price

    def action_reject(self):
        print("action_reject")
        for rec in self:
            rec.status = 'refused'

    _price_positive = models.Constraint(
        'CHECK(price >= 0)',
        'The offer price must be positive.',
    )
