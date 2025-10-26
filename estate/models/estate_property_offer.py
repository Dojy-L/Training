# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api,_
from odoo.exceptions import UserError


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

    def action_accept(self):
        self.ensure_one()
        if 'accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Only one Offer accepted"))
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.partner_id = rec.partner_id.id
            rec.property_id.selling_price = rec.price

    def action_refuse(self):
        for rec in self:
            rec.status = 'refused'

    _price_positive = models.Constraint(
        'check(price < 0)',
        'The Offer Price must be Positive.',
    )