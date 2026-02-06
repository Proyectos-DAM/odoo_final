# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Matricula(models.Model):
    """Modelo Matrícula - Inscripción de alumno a una sesión con flujo de estados"""
    _name = 'edu.matricula'
    _description = 'Matrícula'

    name = fields.Char(string='Referencia', compute='_compute_name', store=True)
    
    # Estado de la matrícula: Borrador -> Confirmada -> Pagada
    state = fields.Selection([
        ('borrador', 'En Borrador'),
        ('confirmada', 'Confirmada'),
        ('pagada', 'Pagada'),
    ], string='Estado', default='borrador', required=True)
    
    fecha_matricula = fields.Date(string='Fecha de Matrícula', default=fields.Date.today)
    fecha_confirmacion = fields.Date(string='Fecha de Confirmación', readonly=True)
    fecha_pago = fields.Date(string='Fecha de Pago', readonly=True)
    
    importe = fields.Float(string='Importe', compute='_compute_importe', store=True)
    notas = fields.Text(string='Notas')
    
    # Relaciones
    alumno_id = fields.Many2one('edu.alumno', string='Alumno', required=True)
    sesion_id = fields.Many2one('edu.sesion', string='Sesión', required=True)
    curso_id = fields.Many2one(
        'edu.curso', 
        string='Curso', 
        related='sesion_id.curso_id', 
        store=True, 
        readonly=True
    )
    
    @api.depends('alumno_id', 'sesion_id')
    def _compute_name(self):
        """Genera el nombre de referencia automáticamente"""
        for record in self:
            if record.alumno_id and record.sesion_id:
                record.name = f'MAT/{record.alumno_id.nombre[:3].upper()}/{record.sesion_id.name[:10]}'
            else:
                record.name = 'Nueva Matrícula'
    
    @api.depends('sesion_id', 'sesion_id.curso_id', 'sesion_id.curso_id.precio')
    def _compute_importe(self):
        """El importe viene del precio del curso"""
        for record in self:
            if record.sesion_id and record.sesion_id.curso_id:
                record.importe = record.sesion_id.curso_id.precio
            else:
                record.importe = 0.0
    
    @api.constrains('alumno_id', 'sesion_id')
    def _check_duplicado(self):
        """Evita matrículas duplicadas del mismo alumno en la misma sesión"""
        for record in self:
            duplicado = self.search([
                ('id', '!=', record.id),
                ('alumno_id', '=', record.alumno_id.id),
                ('sesion_id', '=', record.sesion_id.id),
            ])
            if duplicado:
                raise ValidationError(
                    f'El alumno "{record.alumno_id.nombre}" ya está matriculado '
                    f'en la sesión "{record.sesion_id.name}".'
                )
    
    def action_confirmar(self):
        """Acción para confirmar la matrícula"""
        for record in self:
            if record.state != 'borrador':
                raise ValidationError('Solo se pueden confirmar matrículas en estado Borrador.')
            record.write({
                'state': 'confirmada',
                'fecha_confirmacion': fields.Date.today(),
            })
            # Agregar el alumno a la sesión automáticamente
            record.sesion_id.write({
                'alumno_ids': [(4, record.alumno_id.id)]
            })
    
    def action_pagar(self):
        """Acción para marcar como pagada la matrícula"""
        for record in self:
            if record.state != 'confirmada':
                raise ValidationError('Solo se pueden pagar matrículas en estado Confirmada.')
            record.write({
                'state': 'pagada',
                'fecha_pago': fields.Date.today(),
            })
    
    def action_cancelar(self):
        """Acción para volver a borrador"""
        for record in self:
            if record.state == 'pagada':
                raise ValidationError('No se pueden cancelar matrículas ya pagadas.')
            # Quitar el alumno de la sesión si estaba confirmada
            if record.state == 'confirmada':
                record.sesion_id.write({
                    'alumno_ids': [(3, record.alumno_id.id)]
                })
            record.write({
                'state': 'borrador',
                'fecha_confirmacion': False,
            })
