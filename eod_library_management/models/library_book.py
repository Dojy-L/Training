# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class LibrayBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'


    name = fields.Char(string='Title', required=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    isbn = fields.Char(string='ISBN', required=True)
    summary = fields.Text(string='Summary')
    available_copies = fields.Integer(string='Available Copies', default=1)
    image = fields.Binary(string='Book Image')
    book_rent = fields.Float(string='Book Rent')

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The name must be unique!',
    )

    _unique_isbn = models.Constraint(
        'UNIQUE(isbn)',
        'The ISBn number must be unique!',
    )