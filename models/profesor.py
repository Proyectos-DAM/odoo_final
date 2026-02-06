# -*- coding: utf-8 -*-
from odoo import fields, models


class Profesor(models.Model):
    """Modelo Profesor"""
    _name = 'edu.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre', required=True)
    titulacion = fields.Char(string='Titulación')
    
    # One2One simulado: Un profesor tiene un partner asociado
    partner_id = fields.Many2one('res.partner', string='Contacto')
    
    # One2many: Un profesor puede impartir varios cursos
    curso_ids = fields.One2many('edu.curso', 'profesor_id', string='Cursos que Imparte')
