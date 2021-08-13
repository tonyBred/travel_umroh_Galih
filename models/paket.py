from odoo import models, fields, api, _
from odoo.exceptions import UserError

class paket_hotel_line(models.Model):
    _name = 'paket.hotel.line'

    paket_perjalanan_id = fields.Many2one(
        comodel_name='paket.perjalanan',
        string='Paket Perjalanan',
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Hotel',
        required=True, 
    )
    tgl_awal = fields.Date(string='Start Date', required=True,)
    tgl_akhir = fields.Date(string='End Date', required=True,)
    kota = fields.Char(related="partner_id.city",string='City', readonly=True,)

class paket_pesawat_line(models.Model):
    _name = 'paket.pesawat.line'

    paket_perjalanan_id = fields.Many2one(
        comodel_name='paket.perjalanan',
        string='Paket Perjalanan',
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Airline',
        required=True, 
    )
    tgl_berangkat = fields.Date(string='Departure Date', required=True,)
    kota_asal = fields.Char(string='Departure City', required=True,)
    kota_tujuan = fields.Char(string='Arrival City', required=True,)

class paket_acara_line(models.Model):
    _name = 'paket.acara.line'

    paket_perjalanan_id = fields.Many2one(
        comodel_name='paket.perjalanan',
        string='Paket Perjalanan',
        ondelete='cascade'
    )
    name = fields.Char(string='Name', required=True,)
    tgl = fields.Date(string='Date', required=True,)

class paket_peserta_line(models.Model):
    _name = 'paket.peserta.line'

    paket_perjalanan_id = fields.Many2one(
        comodel_name='paket.perjalanan',
        string='Paket Perjalanan',
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Jamaah',
    )
    name = fields.Char(string='Name in Passport')
    order_id = fields.Many2one(
        comodel_name='sale.order',
        string="Sales Orders",
    )
    gender = fields.Selection([("male","Man"),("female","Woman")], string='Gender')
    tipe_kamar = fields.Selection([('d', 'Double'), ('t', 'Triple'), ('q', 'Quad')], string='Room Type')