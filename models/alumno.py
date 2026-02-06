# -*- coding: utf-8 -*-
from odoo import fields, models


class Alumno(models.Model):
    """Modelo Alumno"""
    _name = 'edu.alumno'
    _description = 'Alumno'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    email = fields.Char(string='Email')
    
    # One2One simulado: Un alumno tiene un partner asociado
    partner_id = fields.Many2one('res.partner', string='Contacto')
    
    # Many2many: Un alumno puede estar en varias clases
    clase_ids = fields.Many2many('edu.clase', string='Clases')
    
    # One2many: Un alumno tiene varias facturas
    facturacion_ids = fields.One2many('edu.facturacion', 'alumno_id', string='Facturas')
