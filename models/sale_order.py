from odoo import models, fields, api, _
from odoo.exceptions import UserError

class sale_order(models.Model):
    _inherit = 'sale.order'

    paket_perjalanan_id = fields.Many2one(
        comodel_name='paket.perjalanan',
        string='Paket Perjalanan',
        domain=[("state", "=", "confirm")],
    )
    dokumen_line = fields.One2many(
        comodel_name='sale.dokumen.line',
        inverse_name='order_id',
        string='Document Lines',
    )
    passport_line = fields.One2many(
        comodel_name='sale.passport.line',
        inverse_name='order_id',
        string='Passport Lines',
    )

    def write(self, vals):
        test = []
        return super(sale_order, self).write(vals)

    # @api.onchange('paket_perjalanan_id')
    # def set_order_line(self):
    #     res = {}
    #     if self.paket_perjalanan_id:
    #         pp = self.paket_perjalanan_id

    #         order = self.env['sale.order'].new({
    #             'partner_id': self.partner_id.id,
    #             'pricelist_id': self.pricelist_id.id,
    #             'date_order': self.date_order
    #         })

    #         line = self.env['sale.order.line'].new({'product_id': pp.product_id.id, 'order_id': order.id})
    #         line.product_id_change()
    #         vals = line._convert_to_write({name: line[name] for name in line._cache})
    #         res['value'] = {'order_line': [vals]}

    #         return res

    @api.onchange('paket_perjalanan_id')
    def set_order_line(self):
        if self.paket_perjalanan_id:
            order = self.env['sale.order'].new({
                'name': self.name,
                'partner_id': self.partner_id.id,
                'partner_invoice_id': self.partner_id.id,
                'partner_shipping_id': self.partner_id.id,
                'pricelist_id': self.pricelist_id.id,
                'company_id': self.company_id.id,
                'date_order': self.date_order,

            })
            pp = self.paket_perjalanan_id
            new_order_line = self.env['sale.order.line'].new({
                'product_id': pp.product_id.id,
                'name': '',
                'order_id': order.id,
                'product_uom_qty' : 1,
            })
            new_order_line.product_id_change()
            self.order_line = new_order_line


class sale_dokumen_line(models.Model):
    _name = 'sale.dokumen.line'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sales Orders',
        ondelete='cascade'
    )
    name = fields.Char(string='Name', required=True,)
    foto = fields.Binary(string='Photo', required=True,)

class sale_passport_line(models.Model):
    _name = 'sale.passport.line'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sales Orders',
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Jamaah',
        required=True,
    )
    room_leader = fields.Many2one(
        comodel_name='res.partner',
        string='Room Leader',
        required=True, 
    )
    room_no = fields.Char(string='Room Number')
    nomor = fields.Char(string='Passport Number', required=True,)
    name = fields.Char(string='Name in Passport', required=True,)
    masa_berlaku = fields.Date(string='Date of Expire', required=True,)
    tipe_kamar = fields.Selection([("d","Double"),("t","Triple"),("q","Quad")], string='Room Type', required=True,)
    foto = fields.Binary(string='Photo', required=True,)
