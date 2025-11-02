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

    property_type_id = fields.Many2one( string="Property Type", related='property_id.property_type_id', store=True)

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline',store=True)


    @api.depends('validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = fields.Date.today() + relativedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.validity = (rec.date_deadline - fields.Date.today()).days

    def action_accept(self):
        if 'accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Only one offer can accept"))
        else:
            for rec in self:
                rec.status = 'accepted'
                rec.property_id.partner_id = self.env.user.partner_id
                rec.property_id.selling_price = rec.price

    def action_reject(self):
        for rec in self:
            rec.status = 'refused'

    _price_positive = models.Constraint(
        'CHECK(price >= 0)',
        'The offer price must be positive.',
    )

    @api.model
    def create(self, vals_list):
        print("CCCCCCCCCCCCCc",vals_list)
        for vals in vals_list:
            print("EEEEEEEEEEEE", vals.get('property_id'), vals.get('price'))
            property_id = vals.get('property_id')
        print("property_idproperty_id------------------->",property_id)
        property_record = self.env['estate.property'].browse(property_id)
        print("property_record------------>",property_record.state,property_record.offer_ids)

        if property_record.offer_ids and vals.get('price'):
            print("MMMMMMMMMMMMMMMMMMMM", max(property_record.offer_ids.mapped('price')))
            max_price = max(property_record.offer_ids.mapped('price'))
            if vals.get('price') < max_price :
                raise UserError("You cant create offer with lower price than existing offer")
        property_record.state = 'received'
        return super().create(vals_list)


