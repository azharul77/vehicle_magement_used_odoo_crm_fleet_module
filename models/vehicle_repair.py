from odoo import models, fields, _, api
from datetime import datetime

from odoo.exceptions import ValidationError


class VehicleRepair(models.Model):
    _name = 'vehicle.repair'
    _description = 'vehicle Repair'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_number = fields.Many2one("vehicle.info", string='Vehicle Number', required=True)
    name = fields.Char(string="Code", readonly=True)
    vehicle_owner = fields.Many2one("res.partner", string='Owner Name ', required=True)
    customer_phone_number = fields.Char(string='Customer Phone Number')
    service_date = fields.Date(string='Date Of Service', required=True)
    service_list = fields.Many2many("vehicle.services", string="Services")
    service_amount_move_id = fields.Many2one(comodel_name="account.move", string="Invoice", track_visibility='onchange', readonly=True)
    invoice_payment_status = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')],
        string='Invoice Status', store=True, readonly=True, copy=False, tracking=True,
        related='service_amount_move_id.invoice_payment_state')

    discount_rate = fields.Float('Discount of %')
    old_customer = fields.Many2one("vehicle.repair", string='Old Customer', readonly=True)
    customer_type = fields.Selection([('old', 'Old Customer'), ('new', 'New Customer'), ], string="Customer Type")
    notes = fields.Text(string='Maintain Customer Detail')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('name_unique', 'unique(name)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.repair')
        res = super(VehicleRepair, self).create(vals)
        self.create_invoice_service(res)

        return res

    def create_invoice_service(self, record):
        if record:
            if record.customer_type == 'new':
                if not record.service_amount_move_id:

                    invoice_line_ids = []
                    for x in record.service_list:
                        invoice_line_ids.append([0, 0, {
                            'product_id': x.service_product.id,
                            'name': x.service_product.name,
                            'account_id': False,
                            'price_unit': x.service_product.list_price,
                            'quantity': 1.0,
                            'discount': 0.0,
                            'product_uom_id': x.service_product.uom_id.id,
                        }])

                    account_move = self.env['account.move'].sudo().create({
                        'name': "INV/Vehicle/" + str(datetime.now().year) + "/" + str(record.id) + "/" + str(record.vehicle_owner.name),
                        'partner_id': record.id,
                        'ref': str(record.vehicle_owner.name),
                        'type': 'out_invoice',
                        'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'invoice_line_ids': invoice_line_ids,
                    })
                    if account_move:
                        invoice_post_status = account_move.sudo().action_post()
                        record.sudo().write({
                            'service_amount_move_id': account_move.id,
                        })
            else:
                if not record.service_amount_move_id:

                    invoice_line_ids = []

                    discount_rate = record.discount_rate
                    for x in record.service_list:
                        invoice_line_ids.append([0, 0, {
                            'product_id': x.service_product.id,
                            'name': x.service_product.name,
                            'account_id': False,
                            'price_unit': x.service_product.list_price,
                            'quantity': 1.0,
                            'discount': discount_rate,
                            'product_uom_id': x.service_product.uom_id.id,
                        }])

                    account_move = self.env['account.move'].sudo().create({
                        'name': "INV/Vehicle/" + str(datetime.now().year) + "/" + str(record.id) + "/" + str(record.vehicle_owner.name),
                        'partner_id': record.id,
                        'ref': str(record.vehicle_owner.name),
                        'type': 'out_invoice',
                        'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'invoice_line_ids': invoice_line_ids,

                    })
                    if account_move:
                        invoice_post_status = account_move.sudo().action_post()
                        record.sudo().write({
                            'service_amount_move_id': account_move.id,
                        })

    @api.onchange('vehicle_number')
    def onchange_vehicle_number_id(self):
        if self.vehicle_number:
            old_customer_id = self.search([('vehicle_number', '=', self.vehicle_number.id)], order='id desc', limit=1)
            self.old_customer = old_customer_id.id if old_customer_id else False

    @api.onchange('vehicle_number')
    def onchange_vehicle_number(self):
        for rec in self:
            if rec.vehicle_number:
                rec.vehicle_owner = rec.vehicle_number.vehicle_owner
                rec.customer_phone_number = rec.vehicle_number.vehicle_owner.phone
                old_customer_id = self.search([('vehicle_number', '=', self.vehicle_number.id)], order='id desc', limit=1)
                if old_customer_id:
                    self.customer_type = 'old'
                else:
                    self.customer_type = 'new'

