from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomerPortalRental(CustomerPortal):

    @http.route(['/my/rentals'], type='http', auth="user", website=True)
    def portal_my_rentals(self, **kw):
        user_partner = request.env.user.partner_id
        print("user_partner---------------------->",user_partner.id)
        rentals = (request.env['book.rental'].sudo().search([
            ('renter_id', '=', user_partner.id),
        ]))
        # '|',('create_uid', '=', request.uid)

        print("rentals--------------->",rentals.mapped('renter_id'))
        return request.render('eod_library_management.portal_my_rentals_template', {
            'rentals': rentals,
            'page_name': 'my_rentals',
        })
