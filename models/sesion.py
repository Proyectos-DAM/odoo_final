# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Sesion(models.Model):
    _name = 'edu.sesion'
    _description = 'Sesión'

    name = fields.Char(string='Nombre', required=True)
    fecha_inicio = fields.Datetime(string='Fecha de Inicio')
    fecha_fin = fields.Datetime(string='Fecha Fin', compute='_compute_fecha_fin', store=True)
    duracion = fields.Float(string='Duración (horas)')
    num_asientos = fields.Integer(string='Número de Asientos')
    
    # Many2one: Una sesión pertenece a un curso
    curso_id = fields.Many2one('edu.curso', string='Curso', required=True)
    
    # Many2one: Una sesión tiene un profesor
    profesor_id = fields.Many2one('edu.profesor', string='Profesor')
    
    # Many2many: Una sesión tiene varios alumnos matriculados
    alumno_ids = fields.Many2many('edu.alumno', string='Alumnos Matriculados')
    
    # Campos computados para ocupación
    asientos_ocupados = fields.Integer(
        string='Asientos Ocupados',
        compute='_compute_ocupacion'
    )
    porcentaje_ocupacion = fields.Integer(
        string='% Ocupación',
        compute='_compute_ocupacion'
    )
    color = fields.Integer(string='Color', compute='_compute_color')
    
    @api.depends('fecha_inicio', 'duracion')
    def _compute_fecha_fin(self):
        for sesion in self:
            if sesion.fecha_inicio and sesion.duracion:
                sesion.fecha_fin = sesion.fecha_inicio + timedelta(hours=sesion.duracion)
            else:
                sesion.fecha_fin = sesion.fecha_inicio

    @api.depends('alumno_ids', 'num_asientos')
    def _compute_ocupacion(self):
        for sesion in self:
            sesion.asientos_ocupados = len(sesion.alumno_ids)
            if sesion.num_asientos > 0:
                sesion.porcentaje_ocupacion = int((sesion.asientos_ocupados / sesion.num_asientos) * 100)
            else:
                sesion.porcentaje_ocupacion = 0
    
    @api.depends('porcentaje_ocupacion')
    def _compute_color(self):
        for sesion in self:
            if sesion.porcentaje_ocupacion >= 100:
                sesion.color = 1  # Rojo - Llena
            elif sesion.porcentaje_ocupacion >= 50:
                sesion.color = 3  # Amarillo/Naranja - Casi llena
            else:
                sesion.color = 10  # Verde - Disponible
    
    @api.onchange('alumno_ids')
    def _onchange_alumno_ids(self):
        if self.num_asientos > 0 and len(self.alumno_ids) > self.num_asientos:
            raise ValidationError(
                f'No hay suficientes asientos disponibles. '
                f'La sesión "{self.name}" tiene {self.num_asientos} asientos '
                f'pero se intentan inscribir {len(self.alumno_ids)} alumnos.'
            )

    @api.constrains('alumno_ids', 'num_asientos')
    def _check_asientos_disponibles(self):
        for sesion in self:
            if sesion.num_asientos > 0 and len(sesion.alumno_ids) > sesion.num_asientos:
                raise ValidationError(
                    f'No hay suficientes asientos disponibles. '
                    f'La sesión "{sesion.name}" tiene {sesion.num_asientos} asientos '
                    f'pero se intentan inscribir {len(sesion.alumno_ids)} alumnos.'
                )
    
    @api.constrains('profesor_id', 'fecha_inicio', 'duracion')
    def _check_profesor_disponible(self):
        for sesion in self:
            if not sesion.profesor_id or not sesion.fecha_inicio:
                continue
            
            # Buscar otras sesiones del mismo profesor
            domain = [
                ('id', '!=', sesion.id),
                ('profesor_id', '=', sesion.profesor_id.id),
            ]
            otras_sesiones = self.search(domain)
            
            for otra in otras_sesiones:
                if not otra.fecha_inicio:
                    continue
                # Verificar solapamiento usando fecha_inicio y fecha_fin
                fin_actual = sesion.fecha_inicio + timedelta(hours=sesion.duracion)
                fin_otra = otra.fecha_inicio + timedelta(hours=otra.duracion)
                
                # Hay solapamiento si los rangos se intersectan
                if sesion.fecha_inicio < fin_otra and fin_actual > otra.fecha_inicio:
                    raise ValidationError(
                        f'El profesor "{sesion.profesor_id.name}" ya tiene asignada '
                        f'la sesión "{otra.name}" en un horario que se solapa.'
                    )
