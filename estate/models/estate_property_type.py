# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate Property Type'
    _order = 'name, sequence desc' # Default ordering in list/tree views

    name = fields.Char(string="Name", required=True)
    # === SQL Constraint (Unique Field) ===
    # Ensures that property type names are unique in the database
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique!',
    )

    # One2many relation to 'estate.property'
    # This means one property type can be linked to multiple property records.
    property_ids = fields.One2many('estate.property','property_type_id',string="Properties")


    sequence = fields.Integer(default=1)

    # To add the state button inside the estate property type form view
    offer_ids = fields.One2many('estate.property.offer','property_type_id')

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        """Compute the number of offers related to this property type."""
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_offers(self):
        """Opens a list/form view of all property offers related to the current property type.
        This method is typically called when clicking a smart button in the form view."""
        return {
            "name": _("Property Offers"),   # Window title
            "type": "ir.actions.act_window",    # Action type (open a new window)
            "target": "current",   # Open in the current window
            "res_model": "estate.property.offer",   # Model to display
            'view_mode': 'list,form',    # View modes to use
            "domain": [('property_type_id', '=', self.id)],   # Filter offers related to this property type
            "context": {'default_property_type_id': self.id},   # Default context for new offer records
        }
