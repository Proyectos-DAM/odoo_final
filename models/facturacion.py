# -*- coding: utf-8 -*-
from odoo import fields, models


class Facturacion(models.Model):
    """Modelo Facturación"""
    _name = 'edu.facturacion'
    _description = 'Facturación'

    name = fields.Char(string='Referencia')
    cantidad = fields.Float(string='Cantidad', required=True)
    fecha_pago = fields.Date(string='Fecha de Pago')
    concepto = fields.Selection([
        ('matricula', 'Matrícula'),
        ('mensualidad', 'Mensualidad'),
        ('material', 'Material'),
        ('otro', 'Otro'),
    ], string='Concepto', default='mensualidad')
    
    # Many2one: Una factura pertenece a un alumno
    alumno_id = fields.Many2one('edu.alumno', string='Alumno', required=True)
