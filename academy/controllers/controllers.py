# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class AcademyController(http.Controller):

    @http.route('/academy/courses', auth='public', type='http')
    def list_courses(self, **kw):
        """
        Devuelve el catálogo de cursos.
        """
        courses = request.env['academy.course'].sudo().search([])

        lines = [course.display_name for course in courses]

        return request.make_response(
            '\n'.join(lines),
            headers=[('Content-Type', 'text/plain; charset=utf-8')]
        )
