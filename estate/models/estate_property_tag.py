# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate Property Tag'
    _order = 'name'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="color")

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique!',
    )