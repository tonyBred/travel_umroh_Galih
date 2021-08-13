import base64
import xlsxwriter
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO

class TravelPackage(models.Model):
    _name = 'paket.perjalanan'

    name = fields.Char(string='Reference', readonly=True, default='/')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True, 
    )
    tgl_berangkat = fields.Date(string='Departure Date', required=True,)
    tgl_pulang = fields.Date(string='Return Date', required=True,)
    quota = fields.Integer(string='Quota')
    quota_progress = fields.Float(string='Quota Progress', compute='_compute_quota_progress',)
    note = fields.Text(string='Notes')
    hotel_line = fields.One2many(
        comodel_name='paket.hotel.line',
        inverse_name='paket_perjalanan_id',
        string='Hotel Lines',
    )
    pesawat_line = fields.One2many(
        comodel_name='paket.pesawat.line',
        inverse_name='paket_perjalanan_id',
        string='Airline Lines',
    )
    acara_line = fields.One2many(
        comodel_name='paket.acara.line',
        inverse_name='paket_perjalanan_id',
        string='Schedule Hotels',
    )
    peserta_line = fields.One2many(
        comodel_name='paket.peserta.line',
        inverse_name='paket_perjalanan_id',
        string='Jamaah Hotels',
        readonly=True,
    )
    state = fields.Selection(
        [("draft","Draft"),("confirm","Confirmed")], 
        string='Status', readonly=True, copy=False, default="confirm", track_visibility="onchange"
    )
    filename = fields.Char(string='Filename')
    data_file = fields.Binary(string='Data file')

    def cetak_jamaah_xls(self):
        # Membuat Worksheet
        folder_title = "Manifest" + "-" + self.name + ".xlsx"
        file_data = BytesIO()
        workbook = xlsxwriter.Workbook(file_data)
        ws = workbook.add_worksheet((self.name))  

		# Menambahkan style
        style = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': True,'fg_color': '#339966','font_color': 'white','align':'center'})
        style.set_text_wrap()
        style.set_align('vcenter')
        style_bold = workbook.add_format({'left': 1, 'top': 1,'right':1,'bottom':1,'bold': True,'align':'center','num_format':'_(Rp* #,##0_);_(Rp* (#,##0);_(* "-"??_);_(@_)'})
        style_bold_gray = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': True,'align':'center','fg_color': '#808080','font_color': 'white'})
        style_no_bold = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': False,'align':'left',})
        style_date = workbook.add_format({'left': 1, 'top': 1,'right':1,'bold': False,'align':'left','num_format': 'dd/mm/yy'})

        # Jamaah

         # Membuat Column Header
        ws.merge_range('A1:D1', 'Manifest' + ' ' + self.name, style_bold)
        ws.set_column(1, 1, 9)
        ws.set_column(1, 2, 9)
        ws.set_column(1, 3, 9)
        ws.set_column(1, 5, 9)
        ws.set_column(1, 6, 9)
        ws.set_column(1, 7, 9)
        ws.set_column(1, 8, 9)
        ws.set_column(1, 9, 9)
        ws.set_column(1, 10, 9)
        ws.set_column(1, 11, 9)
        ws.set_column(1, 12, 9)
        ws.set_column(1, 13, 9)
        ws.set_column(1, 14, 9)
        ws.set_column(1, 15, 9)
        ws.set_column(1, 16, 25)
        ws.write(3, 0,'Title', style_bold_gray)
        ws.write(3, 1,'Gender', style_bold_gray)
        ws.write(3, 2, 'Full Name', style_bold_gray)
        ws.write(3, 3, 'Tempat Lahir', style_bold_gray)
        ws.write(3, 4, 'Tanggal Lahir', style_bold_gray)
        ws.write(3, 5, 'No Passport', style_bold_gray)
        ws.write(3, 6, 'Passport Issued', style_bold_gray)
        ws.write(3, 7, 'Passport Expired', style_bold_gray)
        ws.write(3, 8, 'Imgigrasi', style_bold_gray)
        ws.write(3, 9, 'Mahram', style_bold_gray)
        ws.write(3, 10, 'Usia', style_bold_gray)
        ws.write(3, 11, 'NIK', style_bold_gray)
        ws.write(3, 12, 'Order', style_bold_gray)
        ws.write(3, 13, 'Room Type', style_bold_gray)
        ws.write(3, 14, 'Room Leader', style_bold_gray)
        ws.write(3, 15, 'Room No', style_bold_gray)
        ws.write(3, 16, 'Alamat', style_bold_gray)

        row_count = 4
        count = 1

		# Mengisi data pada setiap baris & kolom
        for partner in self.peserta_line.partner_id:
            ws.write(row_count, 0,partner.title.name, style_no_bold)

            if partner.gender == 'male':
                gender = 'Pria'
            else:
                gender = 'Wanita'
            ws.write(row_count, 1,gender, style_no_bold)

            ws.write(row_count, 2,partner.name, style_no_bold)
            ws.write(row_count, 3,partner.place_birth, style_no_bold)
            ws.write(row_count, 4,partner.date_birth, style_date)

            passport_id = []
            passport_id = self.env['sale.passport.line'].search([('order_id.paket_perjalanan_id','=',self.id), ('partner_id.id','=',partner.id),])
            ws.write(row_count, 5,passport_id.nomor, style_no_bold)
            ws.write(row_count, 6,passport_id.order_id.date_order, style_date)
            ws.write(row_count, 7,passport_id.masa_berlaku, style_date)
            
            ws.write(row_count, 8,partner.city, style_no_bold)
            ws.write(row_count, 9,partner.mahram.name, style_no_bold)
            ws.write(row_count, 10,partner.age, style_no_bold)
            ws.write(row_count, 11,partner.no_ktp, style_no_bold)

            ws.write(row_count, 12,passport_id.order_id.name, style_no_bold)

            if passport_id.tipe_kamar == 'd':
                tipe_kamar = 'Double'
            elif passport_id.tipe_kamar == 't':
                tipe_kamar = 'Triple'
            else:
                tipe_kamar = 'Quadruple'
            ws.write(row_count, 13,tipe_kamar, style_no_bold)

            ws.write(row_count, 14,passport_id.room_leader.name, style_no_bold)
            ws.write(row_count, 15,passport_id.room_no, style_no_bold)
            ws.write(row_count, 16,partner.street, style_no_bold)

            count+=1
            row_count+=1

        # Airline

        ws.write(11, 0,'No', style_bold_gray)
        ws.write(11, 1, 'Airlines', style_bold_gray)
        ws.write(11, 2, 'Departure Date', style_bold_gray)
        ws.write(11, 3, 'Departure City', style_bold_gray)
        ws.write(11, 4, 'Arrival City', style_bold_gray)

        row_count = 12
        count = 1
        no = 1

		# Mengisi data pada setiap baris & kolom
        for pesawat in self.pesawat_line:
            ws.write(row_count, 0,no, style_no_bold)
            ws.write(row_count, 1,pesawat.partner_id.name, style_no_bold)
            ws.write(row_count, 2,pesawat.tgl_berangkat, style_date)
            ws.write(row_count, 3,pesawat.kota_asal, style_no_bold)
            ws.write(row_count, 4,pesawat.kota_tujuan, style_no_bold)

            count+=1
            row_count+=1
            no+=1

		# Menyimpan data di field data_file
        workbook.close()        
        out = base64.encodestring(file_data.getvalue())
        self.write({'data_file': out, 'filename': folder_title})

        return self.view_form()
    
    def view_form(self):        
        view = self.env.ref('travel_umroh.paket_perjalanan_form_view')
        return {
            'name': _('Product Report Wizard'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'paket.perjalanan',
            'views': [(view.id, 'form')],
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_confirm(self):
        self.write({'state': 'confirm'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('paket.perjalanan')
        return super(TravelPackage, self).create(vals)

    def name_get(self):
        return [(this.id, this.name + "#" + " " + this.product_id.partner_ref) for this in self]

    @api.depends('quota', 'peserta_line')
    def _compute_quota_progress(self):
        for r in self:
            if not r.quota:
                r.quota_progress = 0.0
            else:
                r.quota_progress = 100.0 * len(r.peserta_line) / r.quota
    
    def update_jamaah(self):
        order_ids = self.env['sale.order'].search([('paket_perjalanan_id', '=', self.id), ('state', 'not in', ('draft', 'cancel'))])
        if order_ids:
            self.peserta_line.unlink()
            for o in order_ids:
                for x in o.passport_line:
                    self.peserta_line.create({
                    'paket_perjalanan_id': self.id,
                    'partner_id': x.partner_id.id,
                    'name': x.name,
                    'order_id': o.id,
                    'gender': x.partner_id.gender,
                    'tipe_kamar': x.tipe_kamar,
                    })