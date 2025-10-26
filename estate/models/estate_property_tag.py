# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate Property Tag'

    name = fields.Char(string="Name", required=True)