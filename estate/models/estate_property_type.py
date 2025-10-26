# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real estate Property Type'

    name = fields.Char(string="Name", required=True)