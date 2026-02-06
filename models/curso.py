# -*- coding: utf-8 -*-
from odoo import fields, models


class Curso(models.Model):
    """Modelo Curso"""
    _name = 'edu.curso'
    _description = 'Curso'

    name = fields.Char(string='Título', required=True)
    description = fields.Text(string='Descripción')
    nivel = fields.Selection([
        ('a1', 'A1'),
        ('a2', 'A2'),
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('c1', 'C1'),
        ('c2', 'C2'),
    ], string='Nivel', default='a1')
    precio = fields.Float(string='Precio')
    
    # One2many: Un curso tiene muchas sesiones
    sesion_ids = fields.One2many('edu.sesion', 'curso_id', string='Sesiones')
    
    # Many2one: Un curso tiene un profesor responsable
    profesor_id = fields.Many2one('edu.profesor', string='Profesor')
