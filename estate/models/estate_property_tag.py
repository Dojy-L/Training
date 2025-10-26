# -*- coding: utf-8 -*-
from enum import UNIQUE

from odoo import models, fields, api
from odoo.tools import unique


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real estate Property Tag'

    name = fields.Char(string="Name", required=True)


    _check_name = models.Constraint(
        'unique(name)',"Name Must Be Unique"
    )