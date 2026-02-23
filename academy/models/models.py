# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcademyCourse(models.Model):
    _name = 'academy.course'
    _description = 'Curso de la Academia'

    name = fields.Char(string='Nombre del curso', required=True)
    duration = fields.Integer(string='Duración (horas)')
    category = fields.Selection([
        ('online', 'Online'),
        ('presencial', 'Presencial'),
    ], string='Modalidad')
    max_students = fields.Integer(string='Plazas máximas')
    enrollment_ids = fields.One2many(
        'academy.enrollment', 'course_id', string='Matrículas')
    available_seats = fields.Integer(
        string='Plazas disponibles',
        compute='_compute_available_seats',
        store=False,
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'El nombre del curso debe ser único.'),
    ]

    @api.depends('max_students', 'enrollment_ids.state')
    def _compute_available_seats(self):
        """
        Calcula las plazas disponibles:
        available_seats = max_students - nro matrículas en estado 'confirmed'
        """
        for course in self:
            confirmed = self.env['academy.enrollment'].search_count([
                ('course_id', '=', course.id),
                ('state', '=', 'confirmed'),
            ])
            course.available_seats = course.max_students - confirmed


class AcademyEnrollment(models.Model):
    _name = 'academy.enrollment'
    _description = 'Matrícula de alumno'
    _order = 'enrollment_date'

    student_name = fields.Char(string='Nombre del alumno', required=True)
    enrollment_date = fields.Date(
        string='Fecha de matrícula', default=fields.Date.today)
    course_id = fields.Many2one(
        'academy.course', string='Curso', ondelete='cascade')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ], string='Estado', default='draft')

    @api.depends('course_id', 'student_name')
    def _compute_display_name(self):
        """
        Sobrescribe el display_name:
        [Nombre del curso] - Nombre del alumno
        """
        for record in self:
            course_name = record.course_id.name or ''
            record.display_name = f"[{course_name}] - {record.student_name}"
