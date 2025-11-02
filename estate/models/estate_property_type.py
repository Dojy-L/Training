# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate Property Type'
    _order = 'name, sequence desc'

    name = fields.Char(string="Name", required=True)

    property_ids = fields.One2many('estate.property','property_type_id',string="Properties")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique!',
    )

    sequence = fields.Integer(default=1)

    offer_ids = fields.One2many('estate.property.offer','property_type_id')
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        print("_compute_offer_count")
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_offers(self):
        print("action_open_offers")
        return {
            "name": _("Property Offers"),
            "type": "ir.actions.act_window",
            "target": "current",
            "res_model": "estate.property.offer",
            'view_mode': 'list,form',
            "domain": [('property_type_id', '=', self.id)],
            "context": {'default_property_type_id': self.id},
        }
