from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class VehicleInfo(models.Model):
    _name = 'vehicle.info'
    _description = 'vehicle record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Vehicle Number', required=True)
    code = fields.Char(string="Code", readonly=True)
    vehicle_type = fields.Selection([
        ('2wheeler', '2 Wheeler'),
        ('3wheeler', '3 Wheeler'),
        ('4wheeler', '4 Wheeler'),
    ], default='2wheeler', String='Vehicle Type')
    vehicle_model = fields.Many2one("fleet.vehicle.model", string='Vehicle Model', required=True)
    vehicle_owner = fields.Many2one("res.partner", string='Owner Name ', required=True)
    customer_phone_number = fields.Char(string='Customer Phone Number')
    # service_date = fields.Date(string='Date Of Servoce', required=True)
    # service_list = fields.Many2many(
    #     "vehicle.services", "vehicle_service_rel", "vehicle_id", "service_id", string="Services")
    # service_product_ids = fields.Many2many(
    #     string='Service Product',
    #     comodel_name='product.product')
    notes = fields.Text(string='Maintain Customer Detail')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('vehicle.info')
        res = super(VehicleInfo, self).create(vals)
        return res

    @api.onchange('vehicle_owner')
    def onchange_vehicle_owner(self):
        for rec in self:
            if rec.vehicle_owner:
                rec.customer_phone_number = rec.vehicle_owner.phone



