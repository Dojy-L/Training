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
        return request.render('eod_library_management.portal_my_rentals_templates', {
            'rentals': rentals,
            'page_name': 'my_rentals',
        })

    # @http.route(['/my/rental/<int:rental_id>'], type='http', auth="user", website=True)
    # def portal_rental_detail(self, rental_id, access_token=None, **kw):
    #     """Display rental detail page"""
    #     try:
    #         rental_sudo = self._document_check_access('book.rental', rental_id, access_token)
    #     except Exception:
    #         return request.redirect('/my')
    #
    #     values = {
    #         'rental': rental_sudo,
    #         'page_name': 'rental',
    #     }
    #
    #     return request.render("eod_library_management.portal_rental_detail_view", values)
