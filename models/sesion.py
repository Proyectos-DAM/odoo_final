# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Sesion(models.Model):
    """Modelo Sesión"""
    _name = 'edu.sesion'
    _description = 'Sesión'

    name = fields.Char(string='Nombre', required=True)
    fecha_inicio = fields.Date(string='Fecha de Inicio')
    hora_inicio = fields.Float(string='Hora de Inicio', help='Hora en formato decimal (ej: 14.5 = 14:30)')
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
    
    @api.depends('alumno_ids', 'num_asientos')
    def _compute_ocupacion(self):
        """Calcula el porcentaje de ocupación de la sesión"""
        for sesion in self:
            sesion.asientos_ocupados = len(sesion.alumno_ids)
            if sesion.num_asientos > 0:
                sesion.porcentaje_ocupacion = int((sesion.asientos_ocupados / sesion.num_asientos) * 100)
            else:
                sesion.porcentaje_ocupacion = 0
    
    @api.depends('porcentaje_ocupacion')
    def _compute_color(self):
        """Cambia el color según el nivel de ocupación:
        - Verde (10): < 50% ocupación
        - Amarillo (3): 50-99% ocupación  
        - Rojo (1): 100% llena
        """
        for sesion in self:
            if sesion.porcentaje_ocupacion >= 100:
                sesion.color = 1  # Rojo - Llena
            elif sesion.porcentaje_ocupacion >= 50:
                sesion.color = 3  # Amarillo/Naranja - Casi llena
            else:
                sesion.color = 10  # Verde - Disponible
    
    @api.onchange('alumno_ids')
    def _onchange_alumno_ids(self):
        """Aviso inmediato al usuario cuando se superan los asientos"""
        if self.num_asientos > 0 and len(self.alumno_ids) > self.num_asientos:
            raise ValidationError(
                f'No hay suficientes asientos disponibles. '
                f'La sesión "{self.name}" tiene {self.num_asientos} asientos '
                f'pero se intentan inscribir {len(self.alumno_ids)} alumnos.'
            )

    @api.constrains('alumno_ids', 'num_asientos')
    def _check_asientos_disponibles(self):
        """Asegura que el número de alumnos inscritos no supere el número de asientos"""
        for sesion in self:
            if sesion.num_asientos > 0 and len(sesion.alumno_ids) > sesion.num_asientos:
                raise ValidationError(
                    f'No hay suficientes asientos disponibles. '
                    f'La sesión "{sesion.name}" tiene {sesion.num_asientos} asientos '
                    f'pero se intentan inscribir {len(sesion.alumno_ids)} alumnos.'
                )
    
    @api.constrains('profesor_id', 'fecha_inicio', 'hora_inicio', 'duracion')
    def _check_profesor_disponible(self):
        """No permite que un profesor dé dos sesiones a la misma hora"""
        for sesion in self:
            if not sesion.profesor_id or not sesion.fecha_inicio:
                continue
            
            # Buscar otras sesiones del mismo profesor en la misma fecha
            domain = [
                ('id', '!=', sesion.id),
                ('profesor_id', '=', sesion.profesor_id.id),
                ('fecha_inicio', '=', sesion.fecha_inicio),
            ]
            otras_sesiones = self.search(domain)
            
            for otra in otras_sesiones:
                # Verificar solapamiento de horarios
                inicio_actual = sesion.hora_inicio
                fin_actual = sesion.hora_inicio + sesion.duracion
                inicio_otra = otra.hora_inicio
                fin_otra = otra.hora_inicio + otra.duracion
                
                # Hay solapamiento si los rangos se intersectan
                if inicio_actual < fin_otra and fin_actual > inicio_otra:
                    raise ValidationError(
                        f'El profesor "{sesion.profesor_id.name}" ya tiene asignada '
                        f'la sesión "{otra.name}" el mismo día ({sesion.fecha_inicio}) '
                        f'en un horario que se solapa.'
                    )
