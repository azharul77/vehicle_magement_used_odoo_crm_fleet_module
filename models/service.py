from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class Services(models.Model):
    _name = 'vehicle.services'
    _description = "Services Table"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Service Name", requird=True)
    code = fields.Char(string="Code", readonly=True)
    service_charge = fields.Integer(string="Service Charge")
    service_product = fields.Many2one(
        string='Service Product',
        comodel_name='product.product')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('vehicle.services')
        res = super(Services, self).create(vals)
        return res

    @api.onchange('service_product')
    def onchange_amount(self):
        for rec in self:
            if rec.service_product:
                rec.service_charge = rec.service_product.lst_price