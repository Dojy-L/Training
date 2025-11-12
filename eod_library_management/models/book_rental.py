# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, exceptions, _
from datetime import date

from odoo.exceptions import UserError


class BookRental(models.Model):
    _name = 'book.rental'
    _description = 'Book Rental'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'order_no'
    _order = 'order_no,due_date asc'

    # name = fields.Char(string='Title')
    order_no = fields.Char(string='Order Number', readonly=True, required=True, copy=False,
                           default=lambda self: _('New'))
    book_id = fields.Many2one('library.book', required=True)
    renter_id = fields.Many2one('res.partner',string ="Customer", required=True, default=lambda self: self.env.user.partner_id)
    start_date = fields.Date(default=fields.Date.today)
    due_date = fields.Date(string="Due Date", readonly=True)
    end_date = fields.Date(string="End Date")
    overdue_days = fields.Integer(compute='_compute_overdue_days', store=True)
    overdue_fine = fields.Float(compute='_compute_overdue_fine', store=True)
    renter_phone = fields.Char(related='renter_id.phone', readonly=True)
    renter_email = fields.Char(related='renter_id.email', readonly=True)
    renter_street = fields.Char(related='renter_id.street', readonly=True)
    # renter_street2 = fields.Char(related='renter_id.street2', readonly=True)
    # renter_city = fields.Char(related='renter_id.city', readonly=True)
    # renter_zip = fields.Char(related='renter_id.zip', readonly=True)
    # renter_state_id = fields.Many2one('res.country.state', related='renter_id.state_id', readonly=True)
    # renter_country_id = fields.Many2one('res.country', related='renter_id.country_id', readonly=True)

    extra_info = fields.Html(string="Extra Information")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rented', 'Rented'),
        ('overdue', 'Overdue'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.depends('due_date', 'end_date')
    def _compute_overdue_days(self):
        today = fields.Date.today()
        for rec in self:
            if rec.end_date:
                rec.overdue_days = max((rec.end_date - rec.due_date).days, 0) if rec.due_date else 0
                rec.state = 'overdue'
            elif rec.due_date and rec.due_date < today:
                rec.overdue_days = (today - rec.due_date).days
                rec.state = 'overdue'
            else:
                rec.overdue_days = 0

    @api.onchange('book_id')
    def _onchange_book_id(self):
        print("BBBBBBBBBBBBBBB--------------->")
        for rec in self:
            if rec.book_id:
                if rec.book_id.available_copies == 0:
                    raise UserError(_("The selected book has no available copies."))

    @api.depends('overdue_days')
    def _compute_overdue_fine(self):
        for rec in self:
            rec.overdue_fine = rec.overdue_days * 2.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('order_no', _('New')) == _('New'):
                vals['order_no'] = self.env['ir.sequence'].next_by_code('book.sequence.no') or _('New')
            renter_id = vals.get('renter_id')
            if renter_id:
                renter = self.env['res.partner'].browse(renter_id)
                overdue_count = self.search_count([
                    ('renter_id', '=', renter.id),
                    ('overdue_days', '>', 0),
                ])
                print("rrrrrrrrrrrr-------------->", renter)
                if overdue_count >= 5:
                    raise exceptions.ValidationError(
                        _("This user already has 5 overdue books.")
                    )
            vals['start_date'] = fields.Date.today()
            vals['due_date'] = fields.Date.today() + relativedelta(months=1)
            vals['state'] = 'draft'

        return super().create(vals_list)

    @api.constrains('end_date')
    def _check_end_date(self):
        for rec in self:
            if rec.end_date and rec.end_date < rec.start_date:
                raise exceptions.ValidationError(_("End date must be after start date."))

    def write(self, vals):
        if 'end_date' in vals and self.end_date:
            raise exceptions.UserError(_("End date cannot be modified once set."))
        return super().write(vals)

    def action_rent(self):
        print("action_rent")
        for rec in self:
            if rec.book_id.available_copies <= 0:
                raise UserError(_("No available copies of this book to rent."))
                # Reduce available copies by 1
            rec.book_id.available_copies -= 1
            rec.state = 'rented'

    def action_return(self):
        print("action_return")
        for rec in self:
            if rec.state == 'rented' and rec.book_id:
                rec.book_id.available_copies += 1
            rec.end_date = fields.Date.today()
            rec.state = 'returned'

    # @api.model
    # def create(self,vals_list):
    #     for vals in vals_list:
    #         print("vvvvvvvvvvvvvvvv",vals)
    #         print("llllllllllll",vals['start_date'])
    #         print("vvvvvvvvvvvvvvvv",vals.get('start_date'))
    #         vals['start_date'] = fields.Date.today()
    #         vals['due_date'] = fields.Date.today() + relativedelta(days=30)
    #
    #
    #     ssss
