# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real estate Property Offer'
    _order = 'price desc'  # Highest offers appear first

    price = fields.Float(string="Price", required=True)
    status = fields.Selection([('accepted', 'accepted'), ('refused', 'refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', String="Buyer", copy=False, required=True)
    property_id = fields.Many2one('estate.property', string="Name", required=True)

    property_type_id = fields.Many2one(string="Property Type", related='property_id.property_type_id', store=True)

    validity = fields.Integer(string="Validity", default=7)
    # Date deadline is computed from 'validity' field and can also update it inversely.
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline', store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        """ Compute the offer's deadline date. The deadline = today's date + validity period (in days)."""

        for rec in self:
            rec.date_deadline = fields.Date.today() + relativedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        """ Compute the validity in days when the user manually changes the deadline date.
                This keeps 'validity' and 'date_deadline' synchronized both ways. """
        for rec in self:
            rec.validity = (rec.date_deadline - fields.Date.today()).days

    def action_accept(self):
        """   Accepts the current offer.
               - Ensures that only one offer per property can be accepted.
               - Updates the property record:
                   * Assigns the buyer to the property.
                   * Sets the selling price to the accepted offer price.
               """
        # Check if another offer has already been accepted for this property
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
        """     Overrides the default create() method to enforce custom business rules
                before creating an offer.
                Rules:
                1. The offer price cannot be lower than the existing highest offer.
                2. When an offer is created, the related property state changes to 'received'.
                3. If any rule is violated, raises a UserError to prevent record creation.
                """
        print("CCCCCCCCCCCCCc", vals_list)
        for vals in vals_list:
            print("EEEEEEEEEEEE", vals.get('property_id'), vals.get('price'))
            property_id = vals.get('property_id')
        print("property_idproperty_id------------------->", property_id)
        property_record = self.env['estate.property'].browse(property_id)
        print("property_record------------>", property_record.state, property_record.offer_ids)

        if property_record.offer_ids and vals.get('price'):
            print("MMMMMMMMMMMMMMMMMMMM", max(property_record.offer_ids.mapped('price')))
            max_price = max(property_record.offer_ids.mapped('price'))
            if vals.get('price') < max_price:
                raise UserError("You cant create offer with lower price than existing offer")
        property_record.state = 'received'
        return super().create(vals_list)
