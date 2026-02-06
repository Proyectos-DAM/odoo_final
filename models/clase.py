# -*- coding: utf-8 -*-
from odoo import fields, models


class Clase(models.Model):
    """Modelo Clase - Horarios y grupos"""
    _name = 'edu.clase'
    _description = 'Clase'

    name = fields.Char(string='Nombre del Grupo', required=True)
    horario = fields.Char(string='Horario')
    aula = fields.Char(string='Aula')
    
    # Many2one: Una clase pertenece a un curso
    curso_id = fields.Many2one('edu.curso', string='Curso')
    
    # Many2one: Una clase tiene un profesor
    profesor_id = fields.Many2one('edu.profesor', string='Profesor')
    
    # Many2many: Una clase tiene varios alumnos
    alumno_ids = fields.Many2many('edu.alumno', string='Alumnos')
