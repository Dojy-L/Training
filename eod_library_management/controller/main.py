from odoo import http
from odoo.http import request


class LibraryController(http.Controller):

    @http.route('/books', type='http', auth='public', website=True)
    def library_books_val(self, **kwargs):
        books = request.env['library.book'].sudo().search([])
        return (request.render('eod_library_management.books_page_template', {
            'books': books
        }))

    @http.route('/fines', type='http', auth='public', website=True)
    def rental_fines_details(self, **kwargs):
        rentals = request.env['book.rental'].sudo().search([('overdue_fine', '>', 0)])
        customer_fines = {}
        for rental in rentals:
            partner = rental.renter_id
            if partner in customer_fines:
                customer_fines[partner] += rental.overdue_fine
            else:
                customer_fines[partner] = rental.overdue_fine

        fines_list = [{'customer': partner, 'total_fine': total} for partner, total in customer_fines.items()]
        return request.render('eod_library_management.books_fine_template', {
            'fines': fines_list
        })



    @http.route('/overdue', type='http', auth='public', website=True)
    def overdue_fines_details(self, **kwargs):
        # Search for rentals that have a positive overdue fine
        overdue_details = request.env['book.rental'].sudo().search(
            [('overdue_fine', '>', 0)],
            order='overdue_fine desc',
            limit=1
        )
        return request.render('eod_library_management.rental_overdue_template', {
            'overdue': overdue_details,
        })

    # @http.route('/fines', type='http', auth='public', website=True)
    # def rental_fines_details(self, **kwargs):
    #     fine_details = request.env['book.rental'].sudo().search([('overdue_fine','>',0)])
    #     print("fine_details-------------------->",fine_details.mapped('renter_id'))
    #     return request.render('eod_library_management.books_fine_template', {
    #         'fines': fine_details
    #     })
